// components/IntroCard.tsx
"use client";

import { ChevronDown, ChevronUp } from "lucide-react";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { materialDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { useState } from "react";

export default function IntroCard() {
  const [expanded, setExpanded] = useState(true);

  const snippet = `def add_numbers(a, b):
    """
    Returns the sum of two numbers.

    Parameters
    ----------
    a: int
        First number
    b: float
        Second number

    Returns
    -------
    sum: int
        The sum of the inputs.
    """
    return a + b`;

  return (
    <div className="bg-muted rounded-xl p-6 shadow-md max-w-7xl mx-auto text-muted-foreground transition-all">
      <div
        className="flex justify-between items-center cursor-pointer"
        onClick={() => setExpanded(!expanded)}
      >
        <h2 className="text-xl font-bold text-foreground">
          WELCOME TO THE HEADER COMMENT ASSESSMENT QUESTIONNAIRE!
        </h2>
        {expanded ? <ChevronUp /> : <ChevronDown />}
      </div>

      {expanded && (
        <div className="mt-4 space-y-4 text-sm leading-relaxed">
          <p>
            Thank you for participating in our study on assessing header
            comments for different languages. We will consider four different
            languages: <strong>Python</strong>, <strong>C++</strong>,{" "}
            <strong>make</strong> (i.e., the language that makefiles are
            expressed in), and <strong>Art</strong> (a textual language to
            define state machines). In each language, a header comment (often
            also called “doc-string”, “header comment”, “in-line comment”) is a
            comment that precedes the definition of a language construct. For
            Python and C++ these constructs are classes, functions, and methods.
            For make, they are rules. And for Art, they are state machines.
          </p>

          <p>
            For instance, as shown below, the header comment for a Python
            function definition would describe:
          </p>
          <ul className="list-decimal list-inside space-y-1">
            <li>What the function does</li>
            <li>The parameters (if any)</li>
            <li>The return value (if any)</li>
            <li>The exceptions (if any)</li>
          </ul>

          <SyntaxHighlighter
            language="python"
            style={materialDark}
            customStyle={{
              borderRadius: "0.5rem",
              padding: "1rem",
              fontSize: "0.8rem",
              backgroundColor: "#1e1e1e",
            }}
          >
            {snippet}
          </SyntaxHighlighter>

          <p>
            Your task is to evaluate header comments such as the one above with
            respect to four criteria:
          </p>
          <ol className="list-decimal list-inside space-y-1">
            <li>
              <strong>Correctness</strong>: The extent to which there are no
              mistakes in the comment
            </li>
            <li>
              <strong>Comprehensiveness</strong>: The extent to which the
              comment does not omit relevant information
            </li>
            <li>
              <strong>Conciseness</strong>: The extent to which the comment is
              focused, succinctly worded, and avoids unnecessary verbosity
            </li>
            <li>
              <strong>Usefulness</strong>: An overall assessment of the extent
              to which the comment is helpful and facilitates understanding
            </li>
          </ol>

          <p>
            The questionnaire consists of four sections, one for each language.
            At the beginning of each section, there will be a short introduction
            followed by two code snippets together with their header comments.
            After each (code snippet, comment) pair you are asked to rate the
            quality of the header comment on a 5‑point scale for each of the
            four criteria. At the end of the section, you will be able to
            express how confident you are in your assessment, and leave any
            comments you might have for us (if you don’t—no problem, just leave
            the text field empty).
          </p>

          <p>
            <em>
              Overall, the survey should only take a few minutes to complete.
            </em>
          </p>
        </div>
      )}
    </div>
  );
}
