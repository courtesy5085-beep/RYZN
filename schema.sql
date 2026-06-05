-- ============================================================
-- RYNZ Database Schema
-- Run this in Supabase SQL Editor to set up all tables
-- ============================================================

-- ─── EXTENSIONS ─────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ─── PROFILES ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  full_name TEXT NOT NULL DEFAULT '',
  phone TEXT DEFAULT '',
  bio TEXT DEFAULT '',
  education TEXT DEFAULT '',
  career_goals TEXT DEFAULT '',
  skills JSONB DEFAULT '[]'::jsonb,
  role TEXT DEFAULT 'user' CHECK (role IN ('user', 'pro', 'admin')),
  avatar_url TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS for profiles
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON profiles
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON profiles
  FOR INSERT WITH CHECK (auth.uid() = id);

CREATE POLICY "Service role bypass" ON profiles
  USING (auth.role() = 'service_role');

-- ─── JOBS ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS jobs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title TEXT NOT NULL,
  company TEXT NOT NULL,
  location TEXT DEFAULT '',
  job_type TEXT DEFAULT 'Full-time',
  salary TEXT DEFAULT '',
  description TEXT DEFAULT '',
  skills JSONB DEFAULT '[]'::jsonb,
  apply_url TEXT DEFAULT '',
  is_remote BOOLEAN DEFAULT FALSE,
  is_active BOOLEAN DEFAULT TRUE,
  source TEXT DEFAULT 'manual',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '30 days')
);

ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view active jobs" ON jobs
  FOR SELECT USING (is_active = true);

-- ─── INTERNSHIPS ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS internships (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title TEXT NOT NULL,
  company TEXT NOT NULL,
  location TEXT DEFAULT '',
  duration TEXT DEFAULT '',
  stipend TEXT DEFAULT '',
  description TEXT DEFAULT '',
  skills JSONB DEFAULT '[]'::jsonb,
  apply_url TEXT DEFAULT '',
  deadline DATE,
  is_remote BOOLEAN DEFAULT FALSE,
  is_paid BOOLEAN DEFAULT TRUE,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE internships ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view active internships" ON internships
  FOR SELECT USING (is_active = true);

-- ─── SCHOLARSHIPS ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS scholarships (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title TEXT NOT NULL,
  organization TEXT NOT NULL,
  amount TEXT DEFAULT '',
  country TEXT DEFAULT '',
  degree_level TEXT DEFAULT '',
  field TEXT DEFAULT '',
  description TEXT DEFAULT '',
  apply_url TEXT DEFAULT '',
  deadline DATE,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE scholarships ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view active scholarships" ON scholarships
  FOR SELECT USING (is_active = true);

-- ─── SAVED ITEMS ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS saved_items (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  item_type TEXT NOT NULL CHECK (item_type IN ('job', 'internship', 'scholarship')),
  item_id TEXT NOT NULL,
  item_data JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, item_type, item_id)
);

ALTER TABLE saved_items ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own saved items" ON saved_items
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert saved items" ON saved_items
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own saved items" ON saved_items
  FOR DELETE USING (auth.uid() = user_id);

-- ─── CHAT HISTORY ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS chat_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own chat history" ON chat_history
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert chat messages" ON chat_history
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- ─── RESUME ANALYSES ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS resume_analyses (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  ats_score INTEGER NOT NULL DEFAULT 0,
  overall_grade TEXT DEFAULT 'C',
  target_role TEXT DEFAULT '',
  analysis_data JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE resume_analyses ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own analyses" ON resume_analyses
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert analyses" ON resume_analyses
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- ─── MOCK INTERVIEWS ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS mock_interviews (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  role TEXT NOT NULL,
  difficulty TEXT DEFAULT 'Medium',
  avg_score INTEGER DEFAULT 0,
  questions_count INTEGER DEFAULT 0,
  results JSONB DEFAULT '[]'::jsonb,
  completed_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE mock_interviews ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own interviews" ON mock_interviews
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert interviews" ON mock_interviews
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- ─── INDEXES ──────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_jobs_active ON jobs(is_active, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_jobs_type ON jobs(job_type);
CREATE INDEX IF NOT EXISTS idx_internships_active ON internships(is_active, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_scholarships_country ON scholarships(country, is_active);
CREATE INDEX IF NOT EXISTS idx_scholarships_degree ON scholarships(degree_level);
CREATE INDEX IF NOT EXISTS idx_saved_items_user ON saved_items(user_id, item_type);
CREATE INDEX IF NOT EXISTS idx_chat_history_user ON chat_history(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_profiles_role ON profiles(role);

-- ─── TRIGGERS ─────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_profiles_updated_at
  BEFORE UPDATE ON profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ─── HANDLE NEW USER AUTO-PROFILE ─────────────────────────────
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, email, full_name, role)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(NEW.email, '@', 1)),
    'user'
  )
  ON CONFLICT (id) DO NOTHING;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- ─── SAMPLE DATA ──────────────────────────────────────────────
INSERT INTO jobs (title, company, location, job_type, salary, description, skills, apply_url, is_remote) VALUES
  ('Senior Software Engineer', 'Google', 'Mountain View, CA', 'Full-time', '$180K - $250K', 'Build next-gen infrastructure at Google scale.', '["Python", "Go", "Kubernetes", "Distributed Systems"]', 'https://careers.google.com', true),
  ('ML Engineer', 'OpenAI', 'San Francisco, CA', 'Full-time', '$200K - $300K', 'Work on frontier AI models and infrastructure.', '["PyTorch", "Python", "CUDA", "MLOps"]', 'https://openai.com/careers', false),
  ('Product Manager', 'Stripe', 'Remote', 'Full-time', '$160K - $220K', 'Drive Stripe payments product strategy.', '["Product Strategy", "Analytics", "SQL", "APIs"]', 'https://stripe.com/jobs', true),
  ('Frontend Engineer', 'Vercel', 'Remote', 'Full-time', '$140K - $190K', 'Build the fastest web deployment platform.', '["React", "TypeScript", "Next.js", "Performance"]', 'https://vercel.com/careers', true),
  ('Data Scientist', 'Netflix', 'Los Gatos, CA', 'Full-time', '$170K - $240K', 'Personalization and recommendation systems.', '["Python", "R", "Spark", "ML", "Statistics"]', 'https://jobs.netflix.com', false)
ON CONFLICT DO NOTHING;

INSERT INTO internships (title, company, location, duration, stipend, skills, apply_url, deadline, is_remote, is_paid) VALUES
  ('Software Engineering Intern', 'Google', 'Mountain View, CA', '12 weeks', '$8,500/month', '["Python", "Java", "Algorithms", "Data Structures"]', 'https://careers.google.com', '2025-08-01', false, true),
  ('Data Science Intern', 'Meta', 'Menlo Park, CA', '12 weeks', '$9,000/month', '["Python", "SQL", "ML", "Statistics"]', 'https://metacareers.com', '2025-07-15', false, true),
  ('Product Design Intern', 'Figma', 'Remote', '16 weeks', '$7,000/month', '["Figma", "UX Research", "Prototyping", "Design Systems"]', 'https://figma.com/careers', '2025-07-20', true, true),
  ('AI Research Intern', 'DeepMind', 'London, UK', '6 months', '£6,000/month', '["PyTorch", "Research", "ML Theory", "Mathematics"]', 'https://deepmind.com/careers', '2025-09-01', false, true)
ON CONFLICT DO NOTHING;

INSERT INTO scholarships (title, organization, amount, country, degree_level, field, description, apply_url, deadline) VALUES
  ('Fulbright Foreign Student Program', 'US State Department', 'Full Funding', 'USA', 'Masters/PhD', 'All Fields', 'Fully funded graduate studies in the United States.', 'https://foreign.fulbrightonline.org', '2025-10-01'),
  ('Chevening Scholarship', 'UK Government', 'Full Funding', 'UK', 'Masters', 'All Fields', 'UK government global scholarship programme for emerging leaders.', 'https://chevening.org', '2025-11-05'),
  ('Google PhD Fellowship', 'Google', '$50,000/year', 'USA', 'PhD', 'Computer Science', 'Support for outstanding PhD students in computer science.', 'https://research.google/outreach/phd-fellowship/', '2025-08-01'),
  ('DAAD Scholarship', 'German Academic Exchange', '€934/month', 'Germany', 'Masters/PhD', 'All Fields', 'Study in Germany with full living stipend.', 'https://daad.de', '2025-10-15')
ON CONFLICT DO NOTHING;

-- Done! Your RYNZ database is ready. 🚀
