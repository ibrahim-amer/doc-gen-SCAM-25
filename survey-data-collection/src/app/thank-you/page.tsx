// app/thank-you/page.tsx
// "use client";

import Image from "next/image";

export default function ThankYouPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 px-4">
      <Image
        src="/maselogo.png"
        alt="MASE Lab Logo"
        width={200}
        height={200}
        className="mb-8"
      />
      <h1 className="text-4xl font-semibold mb-4 text-center">Thank You!</h1>
      <p className="text-lg text-center max-w-md">
        We appreciate you taking the time to complete our survey. Your feedback
        helps the MASE Lab improve and grow.
      </p>
    </div>
  );
}
