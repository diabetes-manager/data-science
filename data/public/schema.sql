CREATE TABLE "insulin" (
  "id" int PRIMARY KEY,
  "timestamp" int,
  "amount" float,
  "duration" int,
  "type" text,
  "brand" text,
  "user_id" int
);

CREATE TABLE "user" (
  "id" int PRIMARY KEY,
  "bg_high" int,
  "bg_low" int,
  "bg_target_top" int,
  "bg_target_bottom" int,
  "height" int,
  "weight" int,
  "birthdate" date,
  "gender" text,
  "diagnosis_date" date,
  "diabetes_type" text,
  "username" text,
  "password" text
);

CREATE TABLE "bloodsugar" (
  "id" int PRIMARY KEY,
  "timestamp" int,
  "value" int,
  "user_id" int
);

CREATE TABLE "user_upload" (
  "id" int PRIMARY KEY,
  "timestamp" int,
  "object_store" text,
  "user_id" int,
  "data_source" text,
  "model" text
);

ALTER TABLE "insulin" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("id");

ALTER TABLE "bloodsugar" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("id");

ALTER TABLE "user_upload" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("id");