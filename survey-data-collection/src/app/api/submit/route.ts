import { NextResponse } from "next/server";
import type { SurveyPayload } from "@/types/submission";
import type { UpdateResult } from "mongodb";
import { submitToDB } from "@/lib/db";

export async function POST(request: Request) {
  try {
    const body = (await request.json()) as SurveyPayload;
    const result: UpdateResult = await submitToDB(body);

    // Now TS knows result.upsertedCount exists
    const isNew = (result.upsertedCount ?? 0) > 0;
    const status = isNew ? 201 : 200;

    return NextResponse.json({ success: true, inserted: isNew }, { status });
  } catch (error: any) {
    return NextResponse.json(
      { success: false, message: error.message },
      { status: 500 }
    );
  }
}
