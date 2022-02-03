from util_layer.CommonsUtil import CommonsUtil

ADA_ACCOUNT_ID = 'f76721d8-5b98-4275-b25c-ede12411b917'


def test_get_transactions():
    result = CommonsUtil.get_transactions(ADA_ACCOUNT_ID)

    assert len(result) == 0
