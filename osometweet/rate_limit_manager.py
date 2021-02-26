from datetime import datetime
from osometweet.utils import pause_until

def manage_rate_limits(response):
    """Manage Twitter V2 Rate Limits

    This method takes in a `requests` response object after querying
    Twitter and uses the headers["x-rate-limit-remaining"] and
    headers["x-rate-limit-reset"] headers objects to manage Twitter's
    most common, time-dependent HTTP errors.

    Wiki Reference: https://github.com/osome-iu/osometweet/wiki/Info:-HTTP-Status-Codes-and-Errors
    Twitter Reference: https://developer.twitter.com/en/support/twitter-api/error-troubleshooting

    """
    while True:

        # The x-rate-limit-remaining parameter is not always present.
        #    If it is, we want to use it.
        try:
            # Get number of requests left with our tokens
            remaining_requests = int(response.headers["x-rate-limit-remaining"])

            # If that number is one, we get the reset-time
            #   and wait until then, plus 15 seconds (your welcome Twitter).
            # The regular 429 exception is caught below as well,
            #   however, we want to program defensively, where possible.
            if remaining_requests == 1:
                buffer_wait_time = 15
                resume_time = datetime.fromtimestamp( int(response.headers["x-rate-limit-reset"]) + buffer_wait_time )
                print(f"One request from being rate limited. Waiting on Twitter.\n\tResume Time: {resume_time}")
                pause_until(resume_time)
        
        except Exception as e:
            print("An x-rate-limit-* parameter is likely missing...")
            print(e)

        # Explicitly checking for time dependent errors.
        # Most of these errors can be solved simply by waiting
        # a little while and pinging Twitter again - so that's what we do.
        if response.status_code != 200:

            # Too many requests error
            if response.status_code == 429:
                buffer_wait_time = 15
                resume_time = datetime.fromtimestamp( int(response.headers["x-rate-limit-reset"]) + buffer_wait_time )
                print(f"Too many requests. Waiting on Twitter.\n\tResume Time: {resume_time}")
                pause_until(resume_time)

            # Twitter internal server error
            elif response.status_code == 500:
                # Twitter needs a break, so we wait 30 seconds
                resume_time = datetime.now().timestamp() + 30
                print(f"Internal server error @ Twitter. Giving Twitter a break...\n\tResume Time: {resume_time}")
                pause_until(resume_time)

            # Twitter service unavailable error
            elif response.status_code == 503:
                # Twitter needs a break, so we wait 30 seconds
                resume_time = datetime.now().timestamp() + 30
                print(f"Twitter service unavailable. Giving Twitter a break...\n\tResume Time: {resume_time}")
                pause_until(resume_time)

            # If we get this far, we've done something wrong and should exit
            else:
                raise Exception(
                    "Request returned an error: {} {}".format(
                        response.status_code, response.text
                    )
                )

        # Each time we get a 200 response, exit the function and return the response object
        if response.ok:
            return response