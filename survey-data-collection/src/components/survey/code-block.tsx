"use client";

import { useEffect, useRef } from "react";

import type { FC } from "react";
import { cn } from "@/lib/utils";
import hljs from "highlight.js";

interface CodeBlockProps {
  code: string;
  language?: string;
  className?: string;
}

const CodeBlock: FC<CodeBlockProps> = ({ code, language, className }) => {
  const codeRef = useRef<HTMLElement>(null);

  useEffect(() => {
    if (codeRef.current) {
      hljs.highlightElement(codeRef.current);
    }
  }, [code, language]);

  return (
    <pre
      className={cn(
        "rounded-md shadow-md my-4 bg-gray-50 border border-gray-200",
        // both axes scroll, no-wrap
        "overflow-auto whitespace-pre",
        className
      )}
      // cap height so super long snippets scroll
      style={{ maxHeight: "60vh" }}
    >
      <code ref={codeRef} className={`language-${language || "plaintext"}`}>
        {code}
      </code>
    </pre>
  );
};

export default CodeBlock;
