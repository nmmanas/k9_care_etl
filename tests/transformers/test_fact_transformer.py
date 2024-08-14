class TestFactTransformer:
    """
    This class contains the testing logic for `FactTransformer` class.
    """

    def test_basic_transform(self):
        """
        The `test_basic_transform` function tests the transformation of JSON data using
        a `FactTransformer` class.
        """
        json_data = [
            {
                "fact": "A great fact about dogs!",
                "created_date": "2023-10-02T02:22:00.272Z",
            }
        ]

        from ...etl.transformers import FactTransformer

        data = FactTransformer().transform(json_data)

        assert data == json_data

    def test_clean_whitespace_transformer(self):

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

        from ...etl.transformers import FactTransformer

        clean_data = FactTransformer().clean_whitespaces(data)

        assert clean_data[0]["fact"] == "A great fact about dogs!"
        assert clean_data[1]["fact"] == "This is another fact with new line!"
