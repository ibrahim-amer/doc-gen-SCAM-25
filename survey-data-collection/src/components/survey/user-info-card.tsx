"use client";

import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

import React from "react";
import { useFormContext } from "react-hook-form";

interface Props {
  stepName: string;
  fieldName?: string;
  label?: string;
}

export default function UserInfoCard({ stepName, fieldName, label }: Props) {
  const { control } = useFormContext();

  // Intro step: full userInfo block
  if (stepName === "intro") {
    return (
      <div className="space-y-4 max-w-lg mx-auto">
        {/* Name */}
        <FormField
          control={control}
          name="intro.userInfo.name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <input {...field} className="w-full rounded border px-3 py-2" />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        {/* Profession */}
        {/* <FormField
          control={control}
          name="intro.userInfo.profession"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Profession</FormLabel>
              <FormControl>
                <input {...field} className="w-full rounded border px-3 py-2" />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        /> */}
        {/* Email */}
        <FormField
          control={control}
          name="intro.userInfo.email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <input
                  {...field}
                  type="email"
                  className="w-full rounded border px-3 py-2"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        {/* Years */}
        <FormField
          control={control}
          name="intro.userInfo.yearsOfExperience"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Years of Experience</FormLabel>
              <FormControl>
                <input
                  {...field}
                  type="number"
                  min={0}
                  className="w-full rounded border px-3 py-2"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
      </div>
    );
  }

  // Language experience on survey pages
  if (fieldName && label) {
    return (
      <FormField
        control={control}
        name={`${stepName}.${fieldName}` as const}
        render={({ field }) => (
          <FormItem className="max-w-md mx-auto mb-6">
            <FormLabel>{label}</FormLabel>
            <FormControl>
              <input
                {...field}
                type="number"
                min={0}
                className="w-full rounded border px-3 py-2"
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
    );
  }

  return null;
}
