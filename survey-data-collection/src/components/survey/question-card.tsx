"use client";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";

import CodeBlock from "./code-block";
import Image from "next/image";
import type { Question } from "@/types";
import React from "react";
import { useFormContext } from "react-hook-form";

interface Props {
  question: Question;
  stepName: string;
  index: number;
}

export default function QuestionCard({ question, stepName, index }: Props) {
  const { control } = useFormContext();
  const base = `${stepName}.answers.${index}`;

  type MetricKey = "correct" | "comprehensive" | "concise" | "useful";
  const getMetricAdjective = (type: string): MetricKey => {
    switch (type) {
      case "correctness":
        return "correct";
      case "comprehensiveness":
        return "comprehensive";
      case "conciseness":
        return "concise";
      case "usefulness":
        return "useful";
      default:
        return "correct";
    }
  };

  const labelMetricScale = {
    correct: [
      { 1: "not correct at all" },
      { 2: "mostly incorrect" },
      { 3: "somewhat correct" },
      { 4: "mostly correct" },
      { 5: "completely correct" },
    ],
    comprehensive: [
      { 1: "not comprehensive at all" },
      { 2: "mostly incomprehensive" },
      { 3: "somewhat comprehensive" },
      { 4: "mostly comprehensive" },
      { 5: "completely comprehensive" },
    ],
    concise: [
      { 1: "not concise at all" },
      { 2: "mostly verbose" },
      { 3: "somewhat concise" },
      { 4: "mostly concise" },
      { 5: "completely concise" },
    ],
    useful: [
      { 1: "not useful at all" },
      { 2: "mostly useless" },
      { 3: "somewhat useful" },
      { 4: "mostly useful" },
      { 5: "completely useful" },
    ],
  };

  return (
    <Card className="mb-6 shadow-sm">
      <CardHeader className="bg-card pb-2">
        <CardTitle>Question {index + 1}</CardTitle>
        <CardDescription>{question.question}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4 pt-4">
        {/* 1) Hidden field to carry the questionId */}
        {/* Hidden questionId */}
        <FormField
          control={control}
          name={`${base}.questionId` as const}
          render={({ field }) => (
            <input {...field} type="hidden" value={question.questionId ?? ""} />
          )}
        />

        {question.image && (
          <div className="relative aspect-video w-full overflow-hidden rounded">
            <Image
              src={question.image}
              alt=""
              fill
              style={{ objectFit: "cover" }}
            />
          </div>
        )}

        {question.codeSnippet && (
          <CodeBlock code={question.codeSnippet} language={question.language} />
        )}

        {/* Choice */}
        {question.type === "choice" && question.choices && (
          <FormField
            control={control}
            name={`${base}.choice` as const}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Select your answer:</FormLabel>
                <FormControl>
                  <RadioGroup
                    onValueChange={field.onChange}
                    defaultValue={field.value}
                    className="flex flex-col gap-2"
                  >
                    {question.choices!.map((c) => (
                      <FormItem
                        key={c.value}
                        className="flex items-center gap-2"
                      >
                        <RadioGroupItem
                          value={c.value}
                          id={`${base}-choice-${c.value}`}
                        />
                        <FormLabel htmlFor={`${base}-choice-${c.value}`}>
                          {c.text}
                        </FormLabel>
                      </FormItem>
                    ))}
                  </RadioGroup>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        )}

        {/* Text */}
        {question.type === "text" && (
          <FormField
            control={control}
            name={`${base}.text` as const}
            render={({ field }) => (
              <FormItem>
                <FormLabel>Your answer:</FormLabel>
                <FormControl>
                  <textarea
                    {...field}
                    placeholder="Type your answer…"
                    className="w-full rounded border px-3 py-2"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        )}

        {/* Metrics */}
        {question.type === "metrics" && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {[
              [
                "correctness",
                "How correct is the content of the header comment above?",
              ],
              [
                "comprehensiveness",
                "How comprehensive the content of the header comment above?",
              ],
              [
                "conciseness",
                "How concise is the content of the header comment above?",
              ],
              [
                "usefulness",
                "How useful is the content of the header comment above?",
              ],
            ].map(([key, label]) => (
              <FormField
                key={key}
                control={control}
                name={`${base}.ratings.${key}` as const}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>{label}</FormLabel>
                    <FormControl>
                      <div className="flex gap-2">
                        {(labelMetricScale[getMetricAdjective(key)] || []).map(
                          (item) => {
                            const rating = Number(Object.keys(item)[0]);
                            const labelText = (
                              item as unknown as Record<number, string>
                            )[rating];
                            return (
                              <label
                                key={rating}
                                className="flex items-center gap-1"
                              >
                                <input
                                  type="radio"
                                  value={rating}
                                  checked={field.value === rating}
                                  onChange={() => field.onChange(rating)}
                                />
                                <span className="text-sm">
                                  {rating} <em>({labelText})</em>
                                </span>
                              </label>
                            );
                          }
                        )}
                      </div>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
