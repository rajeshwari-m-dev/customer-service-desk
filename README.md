# Customer Service Desk: Call Classification and Agent Evaluation

An LLM pipeline built with LangChain. It reads customer service call transcripts, finds the type of each call, scores the agent on the right quality checks, and writes a short report with advice.

## How it works

1. **Load** call transcripts from a file
2. **Classify** each call: billing, claims, complaint or general_query (with a confidence score)
3. **Route** each call to the right checks:
   - billing and claims: knowledge accuracy, resolution quality
   - complaint: tone and empathy, resolution quality
   - general_query: knowledge accuracy
4. **Evaluate** the agent on each check (score 1 to 5, with a reason)
5. **Report**: a summary and a list of actions to improve
6. **Save** the results to an Excel file

The LLM answers are forced into a fixed format (Pydantic schemas), so the pipeline can use them safely.

## Tech used

Python, LangChain, FastAPI, OpenAI or Gemini (switchable), pandas, Pydantic, Docker, AWS (ECR, ECS Fargate)

## Project structure

```
app.py            FastAPI app
main.py           script version of the pipeline
src/components/   classification, router, evaluation, aggregation, reporting
src/pipeline/     pipeline and inference
src/utils/        config, data and LLM loaders
config/           labels, model names, scoring range (no secrets)
dockerfile        container image
```

## How to run

```
pip install -r requirements.txt
```

Copy `.env.example` to `.env`. Set `LLM_PROVIDER` to `openai` or `gemini`, and add your own API key. Do not put spaces around `=`.

```
uvicorn app:app --reload
```

Open http://127.0.0.1:8000/docs to try the API in your browser.

| Endpoint | What it does |
|---|---|
| `GET /health` | Checks the app is running |
| `POST /evaluate-file` | Upload a file of calls (Excel or CSV), get the evaluated Excel file back |

Input columns: `call_id`, `agent_name`, `transcript`, `expected_call_type`. The file can be Excel (.xlsx) or CSV. `expected_call_type` is the correct answer you write by hand, to compare with the AI's guess.

## Run with Docker

```
docker build -t customer-service-desk .
docker run -p 8000:8000 --env-file .env customer-service-desk
```

The app is then at http://localhost:8000/docs. Keys come from `.env` at run time and are not stored in the image.

## Deployment on AWS

The Docker image was pushed to Amazon ECR and run on Amazon ECS with Fargate. I tested `/evaluate-file` end to end on the running task.

While deploying, the app failed because the environment variables were missing from the ECS task definition. I found this in the CloudWatch logs, added the variables in a new task revision, and redeployed. The service is now scaled to zero to avoid cost, so there is no live link.

Next step I would take: keep API keys in AWS Secrets Manager instead of plain task variables.

## Data

The course data is private, so it is not in this repo. Use your own file in the format above.

## Credit

Built during the IIT Patna GenAI & Agentic AI course. (Edit this line to say exactly what you wrote yourself.)