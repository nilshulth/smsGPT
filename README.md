# smsGPT: SMS-based Chat Service with GPT Model Integration

smsGPT is a scalable chat service that allows users to interact with a GPT-powered conversational AI through SMS.

## Features
- SMS-Based interaction using Twilio
- GPT-powered conversational AI using OpenAI's API
- Terms of Service acceptance flow
- Adjustable response length to fit the SMS medium

## Getting Started
These instructions will help you set up the project on your local machine for development and testing purposes.

### Prerequisites
- A Twilio account with an SMS-enabled phone number
- An OpenAI account with API key
- Python 3.x, pip, and virtualenv installed

### Installation
1. Clone the repository:
'''
git clone https://github.com/USERNAME/smsGPT cd smsGPT
'''
2. Install required packages:
'''
pip install -r requirements.txt
'''
3. Create a `.env` file in the project root directory with the following contents (replace placeholders with actual values):
'''bash
TWILIO_NUMBER=your_twilio_number
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token 
OPENAI_API_KEY=your_openai_api_key
'''
4. Run the app in a local development environment:
'''
flask run
'''

The application should now be running on `http://127.0.0.1:5000/`.

## Deployment
Here are guides on deploying Flask apps to Heroku and Vercel:

- [Deploying to Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)
- [Deploying to Vercel](https://vercel.com/docs/platform/deployments)

Remember to configure the environment variables on your hosting platform before deploying the app.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.