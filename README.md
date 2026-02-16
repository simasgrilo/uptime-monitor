# Uptime Service Monitor

## A Python-based approach to provide an uptime monitoring service
dashed box
This project is an effort to better understand how uptime service tools work under the hood, of the likes of Uptime or Pingdom, in a cloud-based environment. This service will allow users to authenticate and:

1. Enter one or more URLs to be monitored
2. Configure the frequency of the monitoring (e.g., every 30 seconds, 2 minutes, 1 hour)
3. Define an action to take when the monitored URL is either
    - Too slow to respond with the full requested file (i.e., the request did not return the full response in the specified time frame)
    - Out of service (not responding at all)
4. View historical uptime and data in a graphical form.

The following HLD envisions the resulting architecture.

<img src="docs/HLD.png" width=800 height=500 alt="High Level Design of the uptime monitor service">

Stack used:

- FastAPI version v0.129.0 (latest at the time of writing), due to its versatility and performance (and native Pydantic models that suits well the data models of this application). Also, i already am way familiar with Python, but using Go/Rust for this project seems an interesting approach
- Next.js for frontend part, mainly for an easy-to-use integration with Vercel.

Notes:

- Rate limiting is considered to avoid authentication spam from an IP address perspective, to avoid bot overflowing the service with phantom accounts.
- Caching is considered but the current previewed data pattern does not justify much of a cache, as each of the users will have a specific set of monitoring URLs. As we need to render data near real-time for uptime monitoring, caching this part does not seem to aggregate value.
- The data layer store was initially thought of PostgreSQL, but analyzing a bit more, a Key-value store (e.g., Redis) can benefit the application as the models are fairly straightforward and the data access pattern of (users, URLs) might have a fairly low write:read ratio. The reason for that is that the Uptime monitoring service is beign thought of checking for a URL periodically whther the service is alive, and this will be done in a way that a single URL will be monitored, and the registered users will "subscribe" to the corresponding URLs. The monitoring of the URLs then happens only once per URL.