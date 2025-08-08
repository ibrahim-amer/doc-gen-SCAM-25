import { z } from "zod";

export const SurveyFormSchema = z.object({
  userInfo: z.object({
    name: z.string().optional(),
    // profession: z.string().min(1),
    yearsOfExperience: z.number().min(0),
    email: z.string().email(),
  }),
  languageExperience: z.record(z.string(), z.number().min(0)),
  answers: z.array(
    z.object({
      ratings: z.object({
        correctness: z.number().min(1).max(5).optional(),
        comprehensiveness: z.number().min(1).max(5).optional(),
        conciseness: z.number().min(1).max(5).optional(),
        usefulness: z.number().min(1).max(5).optional(),
      }),
      choice: z.string().optional(),
      text: z.string().optional(),
    })
  ),
});

export type SurveyFormSchemaType = z.infer<typeof SurveyFormSchema>;
