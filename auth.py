"""
RYNZ Authentication – Supabase Auth integration
"""
import streamlit as st
from utils.database import get_supabase_client, get_service_client


def init_session():
    """Initialize all session state keys."""
    defaults = {
        "authenticated": False,
        "user": None,
        "access_token": None,
        "refresh_token": None,
        "chat_history": [],
        "saved_jobs": [],
        "saved_scholarships": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def is_authenticated() -> bool:
    return st.session_state.get("authenticated", False) and st.session_state.get("user") is not None


def login_user(email: str, password: str) -> dict:
    """Log in user via Supabase Auth."""
    try:
        supabase = get_supabase_client()
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})

        if response.user:
            user_id = response.user.id
            # Fetch profile
            profile = _get_or_create_profile(user_id, response.user.email, "", "")

            st.session_state["authenticated"] = True
            st.session_state["access_token"] = response.session.access_token
            st.session_state["refresh_token"] = response.session.refresh_token
            st.session_state["user"] = {
                "id": user_id,
                "email": response.user.email,
                "full_name": profile.get("full_name", email.split("@")[0]),
                "role": profile.get("role", "user"),
                "avatar": profile.get("avatar_url", ""),
                "skills": profile.get("skills", []),
                "bio": profile.get("bio", ""),
            }
            return {"success": True}
        return {"success": False, "error": "Invalid credentials. Please try again."}
    except Exception as e:
        err = str(e)
        if "Invalid login credentials" in err:
            return {"success": False, "error": "Invalid email or password."}
        if "Email not confirmed" in err:
            return {"success": False, "error": "Please verify your email first."}
        return {"success": False, "error": f"Login failed: {err}"}


def signup_user(email: str, password: str, first_name: str, last_name: str) -> dict:
    """Create a new Supabase user account."""
    try:
        supabase = get_supabase_client()
        full_name = f"{first_name} {last_name}".strip()
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {"full_name": full_name, "first_name": first_name, "last_name": last_name}
            }
        })

        if response.user:
            # Create profile record
            try:
                service = get_service_client()
                service.table("profiles").upsert({
                    "id": response.user.id,
                    "email": email,
                    "full_name": full_name,
                    "role": "user",
                    "skills": [],
                    "career_goals": "",
                    "education": "",
                }).execute()
            except Exception:
                pass  # Profile creation non-blocking
            return {"success": True}
        return {"success": False, "error": "Signup failed. Please try again."}
    except Exception as e:
        err = str(e)
        if "already registered" in err.lower() or "already been registered" in err.lower():
            return {"success": False, "error": "An account with this email already exists."}
        return {"success": False, "error": f"Signup failed: {err}"}


def logout_user():
    """Clear session state."""
    try:
        supabase = get_supabase_client()
        supabase.auth.sign_out()
    except Exception:
        pass
    keys_to_clear = ["authenticated", "user", "access_token", "refresh_token", "chat_history"]
    for k in keys_to_clear:
        if k in st.session_state:
            del st.session_state[k]
    st.session_state["authenticated"] = False
    st.session_state["user"] = None


def reset_password(email: str) -> dict:
    """Send password reset email via Supabase."""
    try:
        supabase = get_supabase_client()
        supabase.auth.reset_password_email(email)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _get_or_create_profile(user_id: str, email: str, first_name: str, last_name: str) -> dict:
    """Fetch user profile from DB or create default."""
    try:
        service = get_service_client()
        result = service.table("profiles").select("*").eq("id", user_id).single().execute()
        if result.data:
            return result.data
    except Exception:
        pass
    # Return minimal default
    return {
        "full_name": f"{first_name} {last_name}".strip() or email.split("@")[0],
        "role": "user",
        "skills": [],
        "bio": "",
    }


def update_profile(user_id: str, data: dict) -> dict:
    """Update user profile in DB."""
    try:
        service = get_service_client()
        result = service.table("profiles").update(data).eq("id", user_id).execute()
        if result.data:
            # Refresh session user
            user = st.session_state.get("user", {})
            user.update({k: v for k, v in data.items() if k in ("full_name", "skills", "bio", "career_goals", "education", "phone")})
            st.session_state["user"] = user
            return {"success": True}
        return {"success": False, "error": "Update failed."}
    except Exception as e:
        return {"success": False, "error": str(e)}


def require_auth():
    """Decorator-style auth check – redirects to login if not authenticated."""
    if not is_authenticated():
        st.query_params["page"] = "login"
        st.rerun()
