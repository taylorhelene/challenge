def test_commit_history():
    repo = Repository('test_repo')
    repo.create_repo()
    repo.commit('Initial commit')
    history = repo.view_commit_history()
    assert len(history) == 1
    assert history[0]['message'] == 'Initial commit'
