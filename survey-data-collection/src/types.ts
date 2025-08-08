// /types/index.ts
export type QuestionType = "choice" | "text" | "metrics";

export enum QuestionTypeEnum {
  Choice = "choice",
  Text = "text",
  Metrics = "metrics",
}

export interface Choice {
  text: string;
  value: string;
}

export interface Question {
  type: QuestionType;
  image?: string;
  question: string;
  choices?: Choice[];
  codeSnippet?: string;
  codeSnippetPath?: string;
  questionId?: string;
  language?: string;
  required?: boolean;
}

export interface Page {
  introHtmlPath?: string;
  /** Filled in at runtime from that file */
  introHtml?: string;
  intro?: string;
  languageExperienceField?: string;
  questions: Question[];
}

/**
 * Represents the user information section of the questionnaire.
 */
export interface UserInfo {
  /**
   * The name of the user (optional).
   */
  name?: string;
  /**
   * The profession of the user.
   */
  // profession: string;
  /**
   * The years of experience of the user.
   */
  yearsOfExperience: number;
  /**
   * The email of the user.
   */
  email: string;
}

export interface QuestionPage {
  intro?: string;
  languageExperienceField?: number;

  questions: Question[];
}

/**
 * Represents the entire questionnaire data.
 */
export interface QuestionnaireData {
  userInfo: UserInfo;
  languageExperience?: Record<string, number>;
  pages: {
    introHtmlPath?: string;
    /** Filled in at runtime from that file */
    introHtml?: string;
    intro?: string;
    languageExperienceField?: string; // e.g., "python", "cpp"
    questions: Question[];
  }[];
}
