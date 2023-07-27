# Fulfillment Service App Demo

This app demonstrates the core concepts of a [Fulfillment Service App](https://developers.29next.com/docs/apps/guides/fulfillment-service/) that processes order fulfillments for a store using the [Fulfillment Admin APIs](https://developers.29next.com/docs/api/admin/reference/#tag/fulfillment).

### Features

* [Creating Fulfillment Locations](https://developers.29next.com/docs/apps/guides/fulfillment-service/#fulfillment-locations)  - See example [location create api request wrapper](https://github.com/29next/demo-fulfillment-service-app/blob/0cc598efe20a5460c4645401105f5d4b0ca0ae38/app/stores/api/admin.py#L42).
* [Accepting Fulfillment Requests](https://developers.29next.com/docs/apps/guides/fulfillment-service/#accepting-fulfillment-requests) - See example [fulfillment request reciver](https://github.com/29next/demo-fulfillment-service-app/blob/0cc598efe20a5460c4645401105f5d4b0ca0ae38/app/fulfillments/views.py#L20)
* [Rejecting Fulfillment Requests](https://developers.29next.com/docs/apps/guides/fulfillment-service/#rejecting-fulfillment-requests) - See example [fulfillment request reciver](https://github.com/29next/demo-fulfillment-service-app/blob/0cc598efe20a5460c4645401105f5d4b0ca0ae38/app/fulfillments/views.py#L20)
* [Accepting Cancellation Requests](https://developers.29next.com/docs/apps/guides/fulfillment-service/#accepting-cancellation-requests) - See example [fulfillment request reciver](https://github.com/29next/demo-fulfillment-service-app/blob/0cc598efe20a5460c4645401105f5d4b0ca0ae38/app/fulfillments/views.py#L20)
* [Rejecting Cancellation Requests](https://developers.29next.com/docs/apps/guides/fulfillment-service/#rejecting-cancellation-requests) - See example [fulfillment request reciver](https://github.com/29next/demo-fulfillment-service-app/blob/0cc598efe20a5460c4645401105f5d4b0ca0ae38/app/fulfillments/views.py#L20)
* [Creating Fulfillments](https://developers.29next.com/docs/apps/guides/fulfillment-service/#creating-fulfillments) - See example [create fulfillment api wrapper](https://github.com/29next/demo-fulfillment-service-app/blob/0cc598efe20a5460c4645401105f5d4b0ca0ae38/app/stores/api/admin.py#L95)
* [App Oauth Setup Install Flow](https://developers.29next.com/docs/apps/oauth/) - See [store auth setup flow handler](https://github.com/29next/demo-fulfillment-service-app/blob/0cc598efe20a5460c4645401105f5d4b0ca0ae38/app/stores/views.py#L20)

### Screenshots
|![image](https://github.com/29next/demo-fulfillment-service-app/assets/674282/f3bc695e-6947-4aea-91dc-de28b5351e67)|![image](https://github.com/29next/demo-fulfillment-service-app/assets/674282/085ed071-a124-4da8-b850-1b2e25d269da)|
|:-------------------------:|:-------------------------:|
|![image](https://github.com/29next/demo-fulfillment-service-app/assets/674282/6cb4c679-1991-4211-9069-056177dd7bba)|![image](https://github.com/29next/demo-fulfillment-service-app/assets/674282/0ddf1252-f211-41fa-8675-f37d5c8846a8)|


### How to Setup

This app uses [Django](https://docs.djangoproject.com/en/4.1/intro/install/), you can follow Django install guides to ensure you have Python in your local environment.

#### Create App In Partner Account
The first step is to create an App in your 29 Next Partner Account. You'll need your app Client ID and Client Secret later on in the setup process.

#### Install Dependencies
```
pip install -r requirements.txt
```
#### Setup Public Tunnel

To access your localhost for app development, you can use [Ngrok](https://ngrok.com/) or [LocalTunnel](https://localtunnel.github.io/www/) to create and open a public tunnel to your local machine.


#### Environment Variables

| Variable | Description|
|--- | --- |
|APP_DOMAIN| Your domain when running the app (ie your public tunnel url).|
|CLIENT_ID| Your App Client ID found in your partner account. |
|CLIENT_SECRET| Your App Client Secret found in your partner account. |

To run this Django project, you'll need to set environment variables with your local app domain, app client id and client secret (from your 29 Next app).

You can set these directly in your terminal or create an `.env` file inside the `app` directory.


#### Run Django App

To run the Django app on your local, use the following command.

*Django port needs to match the public tunnel port.*

```
cd app/
python manage.py runserver 0.0.0.0:3333
```

You should now be able to access the app locally. You'll need to create a super user to login with, use the following command:
```
python manage.py createsuperuser
```

The full Django admin is available at `/admin/`

#### Install on Development Store
You can now connect your app to your development store which will initiate the Oauth setup flow and configure Admin API access. :tada:

