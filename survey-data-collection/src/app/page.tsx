// This is a Server Component by default (no "use client")
export const dynamic = "force-dynamic";

import Image from "next/image";
import type { QuestionnaireData } from "@/types";
import { SurveyForm } from "@/components/survey/survey-form";
import { getQuestionnaireData } from "@/actions/questionnaire";

export default async function SurveyPage() {
  // fetch your questionnaire data server‑side
  const data = await getQuestionnaireData();

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-7xl mx-auto bg-white shadow-lg rounded-lg p-8">
        <div className="flex justify-center mb-8">
          <Image
            src="/maselogo.png"
            alt="MASE Lab Logo"
            width={120}
            height={120}
          />
        </div>
        {/* Directly render the client component */}
        <SurveyForm data={data} />
      </div>
    </div>
  );
}
