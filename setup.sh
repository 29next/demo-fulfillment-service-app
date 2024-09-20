#!/bin/bash

setup_app_credentials() {
  # Prompt the user for inputs
  read -p "Enter the APP_DOMAIN: " APP_DOMAIN
  read -p "Enter the CLIENT_ID: " CLIENT_ID
  read -p "Enter the CLIENT_SECRET: " CLIENT_SECRET

  echo "APP_DOMAIN=\"$APP_DOMAIN\"" > app.env
  echo "CLIENT_ID=\"$CLIENT_ID\"" >> app.env
  echo "CLIENT_SECRET=\"$CLIENT_SECRET\"" >> app.env

  echo "app.env file created successfully with the following variables:"
  echo "APP_DOMAIN=\"$APP_DOMAIN\""
  echo "CLIENT_ID=\"$CLIENT_ID\""
  echo "CLIENT_SECRET=\"$CLIENT_SECRET\""
}

read -p "Do you want to set up your app credentials? (yes/no): " setup_choice

# Check if the user input is 'yes'
if [[ "$setup_choice" == "yes" || "$setup_choice" == "y" ]]; then
  setup_app_credentials
else
  echo "App credentials setup skipped."
fi
