// lib/db.ts

import { MongoClient, UpdateResult } from "mongodb";

import type { SurveyPayload } from "@/types/submission";

let uri = process.env.MONGODB_URI;
const dbName = process.env.MONGODB_DB;
const dbUser = process.env.MONGO_INITDB_ROOT_USERNAME;
const dbPassword = process.env.MONGO_INITDB_ROOT_PASSWORD;
const dbPort = process.env.MONGO_DB_PORT || "27017";
const dbCollection =
  process.env.MONGO_DB_SUBMISSIONS_COLLECTION || "submissions";

// Fallback URI construction
if (!uri) {
  if (!dbUser || !dbPassword || !dbName) {
    throw new Error("Missing required MongoDB environment variables");
  }
  uri = `mongodb://${dbUser}:${dbPassword}@db:${dbPort}/${dbName}?authSource=admin`;
}

if (!dbName) throw new Error("Missing MONGODB_DB in environment variables");

// Use a global to cache in dev, so Next.js HMR won't open new connections repeatedly
declare global {
  // eslint-disable-next-line no-var
  var _mongoClientPromise: Promise<MongoClient>;
}

let client: MongoClient;
let clientPromise: Promise<MongoClient>;

if (process.env.NODE_ENV === "development") {
  // In development we use a global variable so we don't create
  // a new connection on every file change
  if (!global._mongoClientPromise) {
    client = new MongoClient(uri);
    global._mongoClientPromise = client.connect();
  }
  clientPromise = global._mongoClientPromise;
} else {
  // In production, it's fine to create a new client for each function
  client = new MongoClient(uri);
  clientPromise = client.connect();
}

async function getCollection() {
  // Wait for the client to connect, then grab your collection
  const client = await clientPromise;
  return client.db(dbName).collection(dbCollection);
}

/**
 * Submits the survey data to the MongoDB database.
 * @param data - The survey data to insert.
 */
export async function submitToDB(data: SurveyPayload): Promise<UpdateResult> {
  const col = await getCollection();
  const email = data.intro.userInfo.email;
  if (!email) throw new Error("Missing email in submission");

  const result = await col.updateOne(
    { "intro.userInfo.email": email },
    {
      $set: { ...data, updatedAt: new Date() },
      $setOnInsert: { createdAt: new Date() },
    },
    { upsert: true }
  );

  return result;
}

// export async function submitToDB(data: any): Promise<void> {
//   try {
//     const client = await clientPromise;
//     const db = client.db(dbName);
//     await db.collection(dbCollection).insertOne(data);
//     console.log("Survey data submitted successfully to MongoDB.");
//   } catch (error) {
//     console.error("Error submitting survey data:", error);
//     throw new Error("Failed to submit survey. Please try again.");
//   }
// }
