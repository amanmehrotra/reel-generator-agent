TOPIC_ANALYZER_PROMPT = """
You are an expert content classifier specialized in motivational content.
Given a short motivational quote or sentence, extract the following:
    1. Theme - the central idea or message in 2-5 words.
    2. Tone - the style (e.g., inspiring, assertive, calm).
    3. Emotion - the primary emotional feeling (e.g., hope, courage, determination).

Input:
{input}

Respond strictly in this **structured JSON format**:
Important: **Do NOT include ```json or ``` in the output. Just return raw parsable JSON only.**

```json
{{
  "theme": "...",
  "tone": "...",
  "emotion": "..."
}}

⚠️ VERY IMPORTANT:
- Respond only with valid JSON.
- Include ALL fields shown above. Do not miss any field.
- Use only the exact field names shown.
- Every opening brace must have a matching closing brace.
- Ensure all strings use double quotes `"` and key-value pairs are separated by commas.
- Do NOT include any explanation, introduction, or code block formatting.
- Do NOT include ```json or ``` anywhere in the output.
- Return **only raw JSON**. No surrounding text, no formatting, just JSON.
- If you return anything else, it will cause a system error.
"""

SCRIPT_SCENE_PROMPT ="""
You are a professional scriptwriter and scene planner for short 1-minute motivational reels.
Given the following motivational quote and theme, do two things:
1. Write a powerful voiceover script.
2. Break the script into exactly 4 scenes (hook, build, climax, end). For each scene, return:
   - Exact lines from the script
   - Scene tag (hook/build/climax/end)
   - 2 short, vivid visual concepts to help find cinematic video footage for this scene (eg. on Pexels). The visual should match the emotion and meaning of the line, and be clearly visible in short 5-10 second clips.
     For example: Scene-text: "You are stronger than your excuses." 
                  Visual_keywords: ["man pushing heavy weights", "determined face close up"]

Input provided-     
Quote: "{quote}"
Theme: "{theme}"

Respond strictly in this JSON format:
Important: **Do NOT include ```json or ``` in the output. Just return raw parsable JSON only.**
{{
  "script": "<full script here>",
  "scenes": [
    {{
      "scene_text": "<exact lines from script>",
      "tag": "hook",
      "visual_keywords": ["keyword1", "keyword2"]
    }}
  ]
}}

VERY IMPORTANT:
- All 4 tags (hook, build, climax, end) MUST be present exactly once.
- The full script MUST be completely covered by the 4 scenes. No script line should be omitted.
- Each line in the script MUST be part of the scene.
- Include ALL fields shown above. Do not miss any field.
- Use only the exact field names shown.
- Every opening brace must have a matching closing brace.
- Ensure all strings use double quotes `"` and key-value pairs are separated by commas.
- Do NOT include any explanation, markdown formatting, or code block syntax.
- Do NOT include ```json or ``` anywhere in the output.
- Return **only valid raw JSON**. Any other content will cause system failure.
"""

VISUAL_STYLE_PROMPT = """
Based on the script: '{script}' and the theme: '{theme}', suggest a visual style including tone, transitions, and filter type for a 1-minute motivational reel.
Respond strictly in this JSON format:
Important: **Do NOT include ```json or ``` in the output. Just return raw parsable JSON only.**
{{
  "style_name": "<style>",
  "color_tone": "<color_tone>",
  "transition_type": "<transition_type>"
}}

⚠️ VERY IMPORTANT:
- Respond only with valid JSON.
- Include ALL fields shown above. Do not miss any field.
- Use only the exact field names shown.
- Every opening brace must have a matching closing brace.
- Ensure all strings use double quotes `"` and key-value pairs are separated by commas.
- Do NOT include any explanation, introduction, or code block formatting.
- Do NOT include ```json or ``` anywhere in the output.
- Return **only raw JSON**. No surrounding text, no formatting, just JSON.
- If you return anything else, it will cause a system error.
"""