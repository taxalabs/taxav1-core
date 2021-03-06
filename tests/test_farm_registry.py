import pytest

import brownie

farmDict = {
    'tokenId': 0,
    'name': 1,
    'size': 2,
    'location': 3,
    'imageHash': 4,
    'soil': 5,
    'season': 6,
    'owner': 7,
    'userIndex': 8,
    'platformIndex': 9
}

token_id = 293730023

@pytest.fixture
def frmregistry_contract(FRMRegistry, accounts):
    yield FRMRegistry.deploy({'from': accounts[0]})

def tokenize_farm(frmregistry_contract, accounts):
    tx = frmregistry_contract.tokenizeLand('Arunga Vineyard', '294.32ha', 'Lyaduywa, Kenya', 'QmUfideC1r5JhMVwgd8vjC7DtVnXw3QGfCSQA7fUVHK789', 'loam soil', token_id, {'from': accounts[0]})
    return tx

def test_initial_state(frmregistry_contract):

    # Assertions
    assert frmregistry_contract.totalSupply() == 0
    assert frmregistry_contract.exists(token_id) == False

def test_validate_tokenized_farm(frmregistry_contract, accounts):
    tokenize_farm(frmregistry_contract, accounts)

    # Assertions
    assert frmregistry_contract.exists(token_id) == True

def test_validate_invalid_tokenized_farm(frmregistry_contract):

    # Assertions
    assert frmregistry_contract.exists(2) == False

def test_get_nft_token_name(frmregistry_contract):

    # Assertions
    assert frmregistry_contract.name() == 'Reap'

def test_get_nft_token_symbol(frmregistry_contract):

    # Assertions
    assert frmregistry_contract.symbol() == 'REA'

def test_tokenize_farm(frmregistry_contract, accounts):
    tx = tokenize_farm(frmregistry_contract, accounts)

    # Check log contents
    assert frmregistry_contract.exists(token_id) == True
    assert len(tx.events) == 2
    assert tx.events[1]['_totalFarms'] == 1

def test_get_owner_of_tokenized_farm(frmregistry_contract, accounts):
    tokenize_farm(frmregistry_contract, accounts)

    # Assertions
    assert frmregistry_contract.ownerOf(token_id) == accounts[0]

def test_total_user_tokenized_farms(frmregistry_contract, accounts):
    tokenize_farm(frmregistry_contract, accounts)

    # Assertions
    assert frmregistry_contract.balanceOf(accounts[0]) == 1

def test_total_tokenized_farms(frmregistry_contract, accounts):
    tokenize_farm(frmregistry_contract, accounts)

    # Assertions
    assert frmregistry_contract.totalTokenizedFarms() == 1

def test_query_farms_belonging_to_an_account(frmregistry_contract, accounts):
    tokenize_farm(frmregistry_contract, accounts)
    user_total_farm = frmregistry_contract.balanceOf(accounts[0])
    user_farms = list()
    for i in range(1, user_total_farm+1):
        user_farms.append(frmregistry_contract.queryUserTokenizedFarm(i))

    assert user_total_farm == 1
    assert len(user_farms) == 1
    assert user_farms[0][farmDict['tokenId']] == token_id
    assert user_farms[0][farmDict['name']] == 'Arunga Vineyard'
    assert user_farms[0][farmDict['season']] == 'Dormant'
    assert user_farms[0][farmDict['location']] == 'Lyaduywa, Kenya'

def test_query_all_tokenized_farms(frmregistry_contract, accounts):
    tokenize_farm(frmregistry_contract, accounts)
    total_indexed_farms = frmregistry_contract.totalTokenizedFarms()
    indexed_farms = list()
    for i in range(1, total_indexed_farms+1):
        indexed_farms.append(frmregistry_contract.queryTokenizedFarm(i))

    assert total_indexed_farms == 1
    assert len(indexed_farms) == 1
    assert indexed_farms[0][farmDict['tokenId']] == token_id
    assert indexed_farms[0][farmDict['name']] == 'Arunga Vineyard'
    assert indexed_farms[0][farmDict['season']] == 'Dormant'
    assert indexed_farms[0][farmDict['location']] == 'Lyaduywa, Kenya'

def test_get_tokenized_farm_state(frmregistry_contract, accounts):
    tokenize_farm(frmregistry_contract, accounts)

    # Assertions
    assert frmregistry_contract.getTokenState(token_id) == 'Dormant'

def test_update_tokenized_farm_state(frmregistry_contract, accounts):
    tokenize_farm(frmregistry_contract, accounts)

    frmregistry_contract.transitionState(token_id, 'Preparation', accounts[0])

    # Assertions
    assert frmregistry_contract.getTokenState(token_id) == 'Preparation'

def test_unrestricted_tokenized_farm_state_update(frmregistry_contract, accounts):
    tokenize_farm(frmregistry_contract, accounts)

    # Error assertions
    with brownie.reverts():
        frmregistry_contract.transitionState(token_id, 'Preparation', accounts[1])

def test_update_invalid_tokenized_farm(frmregistry_contract, accounts):
    tokenize_farm(frmregistry_contract, accounts)

    # Error assertions
    with brownie.reverts():
        frmregistry_contract.transitionState(3, 'Planting', accounts[0])

def test_query_tokenized_farm_attached_to_a_token_id(frmregistry_contract, accounts):
    tokenize_farm(frmregistry_contract, accounts)

    farm = frmregistry_contract.getFarm(token_id)

    # Assertions
    assert farm['name'] == 'Arunga Vineyard'
    assert farm['soil'] == 'loam soil'

def test_query_tokenized_farm_attached_to_an_invalid_token_id(frmregistry_contract):

    # Error assertions
    with brownie.reverts():
        frmregistry_contract.getFarm(2)

