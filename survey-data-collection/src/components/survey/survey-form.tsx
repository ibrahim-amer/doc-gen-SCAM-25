"use client";

import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { FormProvider, useForm, useFormContext } from "react-hook-form";
import {
  MultiStepForm,
  MultiStepFormFooter,
  MultiStepFormHeader,
  MultiStepFormStep,
  createStepSchema,
  useMultiStepFormContext,
} from "@/components/ui/multistep-form";

import { Button } from "@/components/ui/button";
import IntroCard from "./intro-card";
import QuestionCard from "./question-card";
import type { QuestionnaireData } from "@/types";
import React from "react";
import { Star } from "lucide-react";
import UserInfoCard from "./user-info-card";
import { cn } from "@/lib/utils";
import { useRouter } from "next/navigation";
import { useToast } from "@/hooks/use-toast";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

// A little component to show "Part X of Y"
function StepIndicator() {
  const { currentStepIndex, totalSteps } = useMultiStepFormContext();
  return (
    <div className="text-center text-lg font-medium mb-6">
      Part {currentStepIndex + 1} of {totalSteps}
    </div>
  );
}

export function SurveyForm({ data }: { data: QuestionnaireData }) {
  const { toast } = useToast();
  const router = useRouter();
  //
  // 1) Build a Zod schema for **every** step.
  //    Intro is strict; each page enforces exactly its fields.
  //
  const schemas: Record<string, z.ZodTypeAny> = {};

  // Intro step
  schemas.intro = z.object({
    userInfo: z.object({
      name: z.string().min(1),
      // profession: z.string().min(1),
      yearsOfExperience: z.coerce.number().min(0),
      email: z.string().email(),
    }),
  });

  // One schema per "pageN"
  data.pages.forEach((page, idx) => {
    const stepKey = `page${idx + 1}`;
    // languageExperience
    const langShape = page.languageExperienceField
      ? { [page.languageExperienceField]: z.coerce.number().min(0) }
      : {};
    // answers: an array of exact-length objects
    // updated
    const answerDef = page.questions.map((q) => {
      // default to true if undefined
      const isRequired = q.required ?? true;

      // always accept the literal questionId
      const idSchema = z.literal(q.questionId!);

      if (q.type === "choice") {
        const schema = isRequired
          ? z.string().min(1, { message: "Please select an option" })
          : z.string().optional();
        return z.object({ choice: schema });
      }

      if (q.type === "text") {
        const schema = isRequired
          ? z.string().min(1, { message: "This field is required" })
          : z.string().optional();
        return z.object({ text: schema });
      }

      // metrics
      const numberSchema = isRequired
        ? z.coerce.number().min(1, { message: "Required" })
        : z.coerce.number().optional();

      return z.object({
        questionId: idSchema,
        ratings: z.object({
          correctness: numberSchema,
          comprehensiveness: numberSchema,
          conciseness: numberSchema,
          usefulness: numberSchema,
        }),
      });
    });

    schemas[stepKey] = z.object({
      languageExperience: z.object(langShape),
      confidence: z.coerce
        .number()
        .min(1, { message: "Please select your confidence level" })
        .max(5),
      answers: z.tuple(
        answerDef as unknown as [z.ZodTypeAny, ...z.ZodTypeAny[]]
      ),
    });
  });

  const schema = createStepSchema(schemas);
  type Values = z.infer<typeof schema>;

  //
  // 2) Build matching defaultValues
  //
  const defaultValues = {} as Values;
  defaultValues.intro = { userInfo: data.userInfo };

  data.pages.forEach((page, idx) => {
    const stepKey = `page${idx + 1}` as keyof Values;
    const langDefaults = page.languageExperienceField
      ? { [page.languageExperienceField]: 0 }
      : {};
    const answersDefaults = page.questions.map((q) => ({
      questionId: q.questionId,
      ...(q.type === "choice"
        ? { choice: "" }
        : q.type === "text"
        ? { text: "" }
        : {
            ratings: {
              correctness: 0,
              comprehensiveness: 0,
              conciseness: 0,
              usefulness: 0,
            },
          }),
    }));
    defaultValues[stepKey] = {
      languageExperience: langDefaults,
      confidence: 0,
      answers: answersDefaults,
    } as any;
  });

  //
  // 3) Hook up React‑Hook‑Form
  //
  const form = useForm<Values>({
    resolver: zodResolver(schema),
    defaultValues,
    mode: "onTouched",
  });

  //
  // 4) Final submission
  //
  const onSubmit = async (vals: Values) => {
    try {
      const res = await fetch("/api/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(vals),
      });
      if (!res.ok) throw new Error();
      toast({ title: "Submitted!", description: "Thank you." });
      router.push("/thank-you");
    } catch {
      toast({
        title: "Error",
        description: "Submission failed.",
        variant: "destructive",
      });
    }
  };

  return (
    <FormProvider {...form}>
      <MultiStepForm schema={schema} form={form} onSubmit={onSubmit}>
        <MultiStepFormHeader>
          <StepIndicator />
        </MultiStepFormHeader>
        {/* Intro Step */}
        <MultiStepFormStep name="intro">
          <IntroCard />
          <div className="mt-8 pt-6 border-t border-gray-200">
            <UserInfoCard stepName="intro" />
          </div>
        </MultiStepFormStep>

        {/* Survey Pages */}
        {data.pages.map((page, idx) => {
          const stepKey = `page${idx + 1}` as keyof Values;
          return (
            <MultiStepFormStep key={stepKey} name={stepKey}>
              {page.introHtml ? (
                <div
                  className="prose max-w-none mb-6"
                  dangerouslySetInnerHTML={{ __html: page.introHtml }}
                />
              ) : page.intro ? (
                <p className="mb-6">{page.intro}</p>
              ) : null}

              {/* {page.languageExperienceField && (
                <UserInfoCard
                  stepName={stepKey}
                  fieldName={`languageExperience.${page.languageExperienceField}`}
                  label={`Years of experience with ${page.languageExperienceField}`}
                />
              )} */}
              <div className="space-y-6">
                {page.questions.map((q, qi) => (
                  <QuestionCard
                    key={qi}
                    question={q}
                    stepName={stepKey}
                    index={qi}
                  />
                ))}
              </div>
              {/* ─── Confidence Separator & Slider ─────────────────────────────── */}
              <div className="mt-8 pt-6 border-t border-gray-200">
                <FormField
                  control={form.control}
                  name={`${stepKey}.confidence` as const}
                  render={({ field }) => (
                    <FormItem className="max-w-md mx-auto">
                      <FormLabel>
                        How confident are you in your answers above?
                      </FormLabel>
                      <FormControl>
                        <div className="px-4">
                          <input
                            type="range"
                            min={1}
                            max={5}
                            step={1}
                            value={field.value}
                            onChange={(e) =>
                              field.onChange(Number(e.target.value))
                            }
                            className="w-full accent-primary"
                          />
                          <div className="flex justify-between text-xs mt-1 text-muted-foreground">
                            {[1, 2, 3, 4, 5].map((n) => (
                              <span key={n}>{n}</span>
                            ))}
                          </div>
                        </div>
                      </FormControl>

                      {/* ─── New star display ─────────────────────────── */}
                      <div className="flex justify-center mt-4 space-x-1">
                        {[1, 2, 3, 4, 5].map((n) => (
                          <Star
                            key={n}
                            size={28}
                            className={cn(
                              field.value >= n
                                ? "text-yellow-500"
                                : "text-gray-300",
                              "transition-colors duration-150"
                            )}
                          />
                        ))}
                      </div>

                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
            </MultiStepFormStep>
          );
        })}

        {/* Footer Navigation */}
        <MultiStepFormFooter>
          <FooterNav />
        </MultiStepFormFooter>
      </MultiStepForm>
    </FormProvider>
  );
}

// ─── FooterNav ────────────────────────────────────────────────────────────────
function FooterNav() {
  const form = useFormContext(); // RHF
  const { prevStep, nextStep, isFirstStep, isLastStep } =
    useMultiStepFormContext(); // MultiStepForm
  const { isSubmitting } = form.formState;

  return (
    <div className="flex justify-between border-t pt-6 mt-6">
      {!isFirstStep && (
        <Button variant="outline" onClick={prevStep} type="button">
          Previous
        </Button>
      )}
      {isLastStep ? (
        <Button type="submit" disabled={isSubmitting}>
          Submit Survey
        </Button>
      ) : (
        <Button
          type="button"
          // This will call the step’s Zod schema under the hood via isStepValid()
          onClick={nextStep}
        >
          Next Page
        </Button>
      )}
    </div>
  );
}
