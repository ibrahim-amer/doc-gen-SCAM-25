// lib/submission.ts

import type { UserInfo } from "@/types"; // your shared type

/** One answer can be choice, text, or metrics. */
export interface ChoiceAnswer {
  questionId: string;
  choice: string;
}
export interface TextAnswer {
  questionId: string;
  text: string;
}
export interface MetricsAnswer {
  questionId: string;
  ratings: {
    correctness: number;
    comprehensiveness: number;
    conciseness: number;
    usefulness: number;
  };
}
export type AnswerSubmission = ChoiceAnswer | TextAnswer | MetricsAnswer;

/** Each “page” of your survey */
export interface PagePayload {
  answers: AnswerSubmission[];
  confidence: number;
  // if you still capture language experience, add it here:
  // languageExperience?: Record<string, number>;
}

/** Full shape of the JSON you POST to /api/submit */
export interface SurveyPayload {
  intro: {
    userInfo: UserInfo;
  };
  /** pages named page1, page2, … */
  [pageKey: `page${number}`]: PagePayload;
}
