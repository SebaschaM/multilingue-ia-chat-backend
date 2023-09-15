INSERT INTO roles (name_role) VALUES ('client') ON CONFLICT DO NOTHING;
INSERT INTO roles (name_role) VALUES ('agent') ON CONFLICT DO NOTHING;
