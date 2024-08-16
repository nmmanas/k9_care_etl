class ErrorReporter:
    def __init__(self, logger, enable_console=False):
        self.logger = logger
        self.enable_console = enable_console
        self.error_log = []

    def report_error(self, message):
        # Log the error to a file and add it to the summary list
        self.logger.error(message)
        self.error_log.append(message)

        # Optionally print the error to the console
        if self.enable_console:
            print(f"Error reported: {message}")

    def send_summary_report(self):
        # Compile the summary report
        summary_message = "Pipeline Summary Report:\n"
        summary_message += (
            "\n".join(self.error_log)
            if self.error_log
            else "No errors occurred."
        )

        # Log the summary report
        self.logger.info(summary_message)

        # Optionally print the summary to the console
        if self.enable_console:
            print(summary_message)

        # Placeholder for future extension: Send summary via email, Slack, etc.
        # For example:
        # self.report_error_via_email(
        #     "Pipeline Summary Report",
        #     summary_message,
        #     "recipient@example.com",
        # )
        # self.report_error_to_slack(summary_message)

    # Placeholder method for future extension (e.g., sending an email)
    def report_error_via_email(self, subject, message, recipient_email):
        pass

    # Placeholder method for future extension (e.g., reporting to Slack)
    def report_error_to_slack(self, message):
        pass
