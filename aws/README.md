# AWS

## Prerequisites

1. The `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` of an IAM user with administrator access. You may follow [this guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/prerequisites.html) to obtain them.
2. The authentification token `TELEGRAM_BOT_TOKEN` of a Telegram bot. You may follow [this guide](https://core.telegram.org/bots#how-do-i-create-a-bot) to obtain it.

## Set Up

1. Configure your working directory with your `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

```bash
% aws configure
```

2. Set ups AWS infrastructure.

```bash
% sam init
% sam build
% sam deploy
```

3. Overwrite placeholder token with your `TELEGRAM_BOT_TOKEN`.

```bash
% TELEGRAM_BOT_TOKEN=<your token>
% aws ssm put-parameter --name TELEGRAM_BOT_TOKEN --value $TELEGRAM_BOT_TOKEN --overwrite
```

4. Set webhook for your Telegram bot.

```bash
% COMMANDS_FUNCTION_URL=$(aws lambda get-function-url-config --function-name HandleCommands --query FunctionUrl --output text)
% curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook?url=$COMMANDS_FUNCTION_URL"
```

## Tear Down

1. Delete webhook for your Telegram bot.

```bash
% TELEGRAM_BOT_TOKEN=$(aws ssm get-parameter --name TELEGRAM_BOT_TOKEN --query Parameter.Value --output text)
% curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/deleteWebhook"
```

2. Delete AWS infrastructure.

```bash
$ sam delete
```
