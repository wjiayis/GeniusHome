# GeniusHome

## Overall Architecture

![architecture diagram](docs/architecture_diagram.svg)

## Implemented Features

- Subscribe to and unsubscribe from user notifications and developer notifications
- Get notifications when it's going to rain

## Cost Breakdown

### Hardware

| Category              | Device          | Quantity | Unit Price (SGD) | Remarks                                                                      |
| --------------------- | --------------- | -------- | ---------------- | ---------------------------------------------------------------------------- |
| Sensor                | BME280          | 1        | $3.82            | <ul><li>temperature</li><li>air pressure</li><li>relative humidity</li></ul> |
| Micro-controller Unit | ESP8266 D1 Mini | 1        | $2.94            |                                                                              |
| Enclosure             | Cuboid Box      | 1        | $2.18            |                                                                              |
| Battery               | AAA             | 4        | $2.29            |                                                                              |
| Miscellaneous         | Thin wire       |          |                  |                                                                              |
|                       | Solder          |          |                  |                                                                              |

### AWS

- User facing

  No cost involved.

- Developer facing

  | Service        | Purpose                | [Always Free Tier](https://aws.amazon.com/free) | [Monthly Cost (SGD)](https://calculator.aws/#/) |
  | -------------- | ---------------------- | ----------------------------------------------- | ----------------------------------------------- |
  | S3             | infrastructure as code | ❌                                              | < $0.005                                        |
  | CloudFormation | infrastructure as code | ✅                                              | 0                                               |
  | CloudWatch     | performance monitoring | ✅                                              | 0                                               |

### Telegram

No cost involved.
