import os
import json
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)

EXTRACTION_PROMPT = """
You are a clinical discharge summary extraction system.

Extract ONLY information explicitly present in the source text.

Never infer.
Never guess.
Never fabricate.

If information is absent:

"value": "MISSING"

If information is mentioned but unresolved:

"value": "PENDING"

For structured fields return the FULL JSON object.

Never return empty objects {}.

Return JSON only.

{
  "patient_demographics": {
    "value": "",
    "evidence": "",
    "confidence": 0.0
  },

  "admission_date": {
    "value": "",
    "evidence": "",
    "confidence": 0.0
  },

  "discharge_date": {
    "value": "",
    "evidence": "",
    "confidence": 0.0
  },

  "principal_diagnosis": {
    "value": "",
    "evidence": "",
    "confidence": 0.0
  },

  "secondary_diagnoses": [],

  "hospital_course": {
    "value": "",
    "evidence": "",
    "confidence": 0.0
  },

  "procedures": [],

  "discharge_medications": [],

  "medication_reconciliation": [],

  "allergies": [],

  "follow_up_instructions": {
    "value": "",
    "evidence": "",
    "confidence": 0.0
  },

  "pending_results": [],

  "discharge_condition": {
    "value": "",
    "evidence": "",
    "confidence": 0.0
  }
}
"""


def extract(text):

    if not text.strip():
        return {}

    print("\n=== INPUT LENGTH ===")
    print(len(text))
    print("====================")

    print("\n=== INPUT SAMPLE ===")
    print(text[:500])
    print("====================")

    try:

        response = None

        for attempt in range(3):

            try:

                response = (
                    client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=
                        EXTRACTION_PROMPT
                        + "\n\nTEXT:\n"
                        + text[:12000]
                    )
                )

                break

            except Exception as e:

                print(
                    f"\nRetry {attempt + 1}/3"
                )

                print(e)

                time.sleep(5)

        if response is None:

            return {
                "principal_diagnosis": {
                    "value": "PENDING",
                    "evidence": "",
                    "confidence": 0.0
                },
                "hospital_course": {
                    "value": "PENDING",
                    "evidence": "",
                    "confidence": 0.0
                },
                "discharge_condition": {
                    "value": "PENDING",
                    "evidence": "",
                    "confidence": 0.0
                }
            }

        print("\n=== GEMINI RESPONSE ===")
        print(response.text)
        print("=======================")

        response_text = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        parsed = json.loads(
            response_text
        )

        print("\n=== PARSED JSON ===")
        print(
            json.dumps(
                parsed,
                indent=2
            )
        )
        print("===================")

        return parsed

    except Exception as e:

        print(
            "\nEXTRACTION ERROR:",
            e
        )

        return {
            "principal_diagnosis": {
                "value": "PENDING",
                "evidence": "",
                "confidence": 0.0
            },
            "hospital_course": {
                "value": "PENDING",
                "evidence": "",
                "confidence": 0.0
            },
            "discharge_condition": {
                "value": "PENDING",
                "evidence": "",
                "confidence": 0.0
            }
        }