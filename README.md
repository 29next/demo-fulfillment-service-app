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

#### Create App In Partner Account
The first step is to create an [App](https://developers.29next.com/docs/apps/) in your [29 Next Partner Account](https://accounts.29next.com/partners/). You'll need your app Client ID and Client Secret later on in the setup process.

You need your App Client ID and Client Secret for the [Oauth install flow](https://developers.29next.com/docs/apps/oauth/).

Take note of your App `Client ID` and `Client Secret`, you'll need it when configuring your app.

#### Install Docker & Docker Compose

The demo app uses Docker and Docker Compose to setup a full development environment with Django, Postgres, Celery, and RabbitMQ.

##### Option 1 - Install Docker Desktop

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)

##### Option 2 - Manual Install

- Install [Docker](https://docs.docker.com/engine/)
- Install [Docker Compose](https://docs.docker.com/compose/)


#### Setup Public Tunnel

To access your localhost for app development, you can use [Ngrok](https://ngrok.com/) or [LocalTunnel](https://localtunnel.github.io/www/) to create and open a public tunnel to your local machine.


Your tunnel should expose port `3000`, take note of your public domain for the next setup.


#### Update your App Oauth Settings

Update your App Oauth **Redirect URLs** to match your local tunnel domain.

```
https://<YOUR LOCAL TUNNEL DOMAIN>/stores/auth/setup/
```


### Configure Your Application

To run the app, we need to configure it to use your local tunnel domain and Oauth credentials.

```bash
source setup.sh
```

This script will configure environment variables in app.env file.


#### Run Application

To run the application on your local, use the following command.

In a new terminal

```bash
docker compose up
```

You should now be able to access the app on your tunnel domain and localy at `localhost:3000`.

#### Migrate Database & Create Super User

With your application now running, you need to migrate the database and create a super user.

In a new terminal, shell into your running django container

```bash
docker compose exec app bash
```

Once inside the container, run this command to migrate the database and create a superuser.

```bash
python manage.py migrate && python manage.py createsuperuser
```

The full Django admin is available at `http://localhost:3000/admin/`

#### Install on Development Store

You can now connect your app to your development store which will initiate the Oauth setup flow and configure Admin API access. :tada:

