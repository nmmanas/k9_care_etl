class TestFactTransformer:
    """
    This class contains the testing logic for `FactTransformer` class.
    """

    def test_clean_whitespace_transformer(self, fact_transformer_instance):
        """
        This function tests the `clean_whitespaces` method of the
        `FactTransformer` class by providing sample data with whitespace to be
        cleaned.
        """

        data = [
            {
                "fact": " A great fact    about dogs!  ",
                "created_date": "2023-10-02T02:22:00.272Z",
            },
            {
                "fact": " This is  another fact with  new line! \n ",
                "created_date": "2023-10-02T02:22:00.272Z",
            },
        ]

        clean_data = fact_transformer_instance.clean_whitespaces(data)

        assert clean_data[0]["fact"] == "A great fact about dogs!"
        assert clean_data[1]["fact"] == "This is another fact with new line!"
