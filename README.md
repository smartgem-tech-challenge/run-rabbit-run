# Run Rabbit Run

This application is designed to control Tapo L530 bulbs by listening to messages from a RabbitMQ queue. The application processes incoming JSON messages and sends commands to control the bulbs, adjusting their on/off state, brightness and colour.

## Installation and Setup

### Requirements

- Python 3.7+
- RabbitMQ server
- API server
- Tapo L530 bulbs connected to the SmartGem local network

### Step-by-Step Setup

1. **Clone the repository**:

```bash
git clone https://github.com/smartgem-tech-challenge/rabbit-runner.git
cd run-rabbit-run
```

2. **Create and activate a virtual environment**:

```bash
python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. **Install required dependencies**:

```bash
pip3 install -r requirements.txt
```

4. **Configure environment variables**:

Create a `.env` file in the project root and add your configuration:

```makefile
API_HOST=
RABBITMQ_HOST=
RABBITMQ_USERNAME=
RABBITMQ_PASSWORD=
RABBITMQ_QUEUE=
TAPO_USERNAME=
TAPO_PASSWORD=
```

5. **Run the application**:

To start listening for messages and controlling bulbs:

```bash
python3 main.py
```