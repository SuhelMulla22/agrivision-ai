-- AgriVision AI — Supabase Database Schema
-- Run this in Supabase SQL Editor: https://supabase.com/dashboard → SQL Editor

-- ============================================================
-- PREDICTIONS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS predictions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id TEXT,
  disease TEXT NOT NULL,
  disease_id TEXT,
  crop TEXT NOT NULL,
  confidence REAL NOT NULL,
  severity TEXT,
  is_healthy BOOLEAN DEFAULT FALSE,
  language TEXT DEFAULT 'en',
  processing_time_ms REAL,
  image_url TEXT,
  top_predictions JSONB,
  disease_info JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for fast history queries
CREATE INDEX IF NOT EXISTS idx_predictions_user_id ON predictions(user_id);
CREATE INDEX IF NOT EXISTS idx_predictions_created_at ON predictions(created_at DESC);

-- Enable Row Level Security
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only read their own predictions
CREATE POLICY "Users can view own predictions"
  ON predictions FOR SELECT
  USING (user_id = auth.uid()::text OR user_id IS NULL);

-- Policy: Anyone can insert predictions (auth optional)
CREATE POLICY "Anyone can insert predictions"
  ON predictions FOR INSERT
  WITH CHECK (true);

-- ============================================================
-- STORAGE BUCKET
-- ============================================================
-- Create a storage bucket for crop images
-- Run in Supabase Dashboard → Storage → New Bucket
-- Name: crop-images
-- Public: Yes

-- ============================================================
-- OPTIONAL: User profiles (if not using Supabase Auth)
-- ============================================================
-- If using the in-app auth (not Supabase Auth), uncomment this:
--
-- CREATE TABLE IF NOT EXISTS user_profiles (
--   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
--   name TEXT NOT NULL,
--   email TEXT UNIQUE NOT NULL,
--   password_hash TEXT NOT NULL,
--   location TEXT,
--   created_at TIMESTAMPTZ DEFAULT NOW()
-- );
