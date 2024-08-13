class TestTransform:
    def test_extract_data(self):
        """
        The function `test_extract_data` extracts and transforms JSON data using a
        helper function.
        """
        json_data = [
            {
                "fact": "A great fact about dogs!",
                "created_date": "2023-10-02T02:22:00.272Z",
            }
        ]

        from ..etl.transform import transform_data

        data = transform_data(json_data)

        assert data == json_data
