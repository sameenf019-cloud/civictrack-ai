# Decisions

1. Scope is a working prototype, not a full FYP. YOLO, duplicate
   detection, voice and Urdu NLP are left for later.
2. SQLite first, PostgreSQL later (avoids Windows PostGIS setup).
   Locations stored as latitude and longitude columns.
3. AI in the prototype is minimal (simple text category suggestion).
   AI results are recommendations only and must be labeled clearly.
4. Stayed with CivicTrack AI instead of switching to another idea.