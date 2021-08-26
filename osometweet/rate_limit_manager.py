"""
This module handles Twitter rate limiting automatically by relying on the
the response objects `x-rate-limit*` parameters as well as HTTP errors.
"""
from datetime import datetime
from osometweet.utils import get_logger, pause_until

logger = get_logger(__name__)

def manage_rate_limits(response):
    """Manage Twitter V2 Rate Limits

    This method takes in a `requests` response object after querying
    Twitter and uses the headers["x-rate-limit-remaining"] and
    headers["x-rate-limit-reset"] headers objects to manage Twitter's
    most common, time-dependent HTTP errors.

    Wiki Reference: https://github.com/osome-iu/osometweet/wiki/Info:-HTTP-Status-Codes-and-Errors
    Twitter Reference: https://developer.twitter.com/en/support/twitter-api/error-troubleshooting
    """

    # The x-rate-limit-remaining parameter is not always present.
    #    If it is, we want to use it.
    try:
        # Get number of requests left with our tokens
        remaining_requests = int(response.headers["x-rate-limit-remaining"])

        # If that number is below 3, we try to get the reset-time
        #   and wait until then, plus 15 seconds (your welcome Twitter).
        # The regular 429 exception is caught below as well,
        #   however, we want to program defensively, where possible.
        # We check if requests are below 3 since this safety net is apparently
        #   not super reliable.
        if remaining_requests < 3:
            logger.info("Running out of requests...")
            buffer_time = 15
            resume_time = datetime.fromtimestamp(
                int(response.headers["x-rate-limit-reset"]) + buffer_time
            )
            logger.info(f"Waiting on Twitter.\n\tResume Time: {resume_time}")
            pause_until(resume_time)
            return True

    except Exception as e:
        logger.info("An x-rate-limit-* parameter is likely missing...")
        logger.info(e)


    # It seems like Twitter's HTTP status code system is also buggy so we need
    # to manually check for the error code no matter what.
    #    Ref: https://twittercommunity.com/t/proper-way-to-handle-rate-limits/150272/5
    if "errors" in response.json():
        # Return the json object so you can see the errors (leave in while we
        # work the quirks out)
        logger.info("Response JSON contains 'errors' object.")
        #logger.info(response.json()["errors"])

        # Lots of information is returned in the 'errors' object by Twitter
        #   that are not official errors. This removes only those with codes
        code_message_dict = [
            dic for dic in response.json()["errors"] if "code" in dic
        ]

        # Create a list of the code integers
        codes = []
        for dic in code_message_dict:
            codes.extend([val for key, val in dic.items() if key == "code"])

        if any([code == 88 for code in codes]):
            logger.info("Too many requests.")
            try:
                buffer_time = 15
                resume_time = datetime.fromtimestamp(
                    int(response.headers["x-rate-limit-reset"]) + buffer_time
                )
                logger.info(
                    f"Waiting on Twitter.\n\tResume Time: {resume_time}"
                )
                pause_until(resume_time)
                return True

            # If there is no x-rate-limit-reset a KeyError should be thrown
            #   In this case, we just wait 5 minutes by default
            except KeyError:
                logger.exception(
                    "An x-rate-limit-* parameter is likely missing..."
                )
                resume_time = datetime.now().timestamp() + (60 * 5)
                pause_until(resume_time)
                return True

            except:
                raise Exception(
                    "Rate limit error detected.\n\n"
                    "Tried waiting some period of time but there appears "
                    "to be another error!! To avoid potential suspension "
                    "due to ignoring rate limit warnings, we break the "
                    "program."
                )

        else:
            logger.info("None of those errors were rate-limit errors.")
            return False

    # Explicitly checking for time dependent errors.
    # Most of these errors can be solved simply by waiting
    # a little while and pinging Twitter again - so that's what we do.
    if response.status_code != 200:

        # Too many requests error
        if response.status_code == 429:
            logger.info(f"Too many requests...")
            buffer_time = 15
            try:
                # Try to use the x-rate-limit-reset to wait on Twitter
                resume_time = datetime.fromtimestamp(
                    int(response.headers["x-rate-limit-reset"]) + buffer_time
                )
                logger.info(f"\n\tResume Time: {resume_time}")
                pause_until(resume_time)
                return True

            except:
                # x-rate-limit was missing
                # so we just default to a 5 minute wait
                resume_time = datetime.now().timestamp() + (60 * 5)
                logger.info(f"\n\tResume Time: {resume_time}")
                pause_until(resume_time)
                return True

        # Twitter internal server error
        elif response.status_code == 500:
            # Twitter needs a break, so we wait 30 seconds
            resume_time = datetime.now().timestamp() + 30
            logger.info(
                "Internal server error @ Twitter. Giving Twitter a break..."
                f"\n\tResume Time: {resume_time}"
            )
            pause_until(resume_time)
            return True

        # Twitter service unavailable error
        elif response.status_code == 503:
            # Twitter needs a break, so we wait 30 seconds
            resume_time = datetime.now().timestamp() + 30
            logger.info(
                "Twitter service unavailable. Giving Twitter a break..."
                f"\n\tResume Time: {resume_time}"
            )
            pause_until(resume_time)
            return True

        # If we get this far, we've done something wrong and should exit
        else:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )

    # If we get this far, we should be error-free
    return False
