pytest_plugins = ['pytester']


def test_group_runs_appropriate_tests(testdir):
    testdir.makepyfile("""
        def test_x(): pass
        def test_y(): pass
        def test_z(): pass
    """)

    result = testdir.runpytest_subprocess('--test-group-count', '2', '--test-group', '1')
    result.assert_outcomes(passed=2)
    result.stdout.fnmatch_lines([
        'Running test group #1 (2 tests)'
    ])

    result = testdir.runpytest_subprocess('--test-group-count', '2', '--test-group', '2')
    result.assert_outcomes(passed=1)
    result.stdout.fnmatch_lines([
        'Running test group #2 (1 tests)'
    ])


def test_group_with_filtering(testdir):
    testdir.makepyfile("""
        def test_a_1(): pass
        def test_a_2(): pass
        def test_a_3(): pass
        def test_a_4(): pass
        
        def test_b_1(): pass
        def test_b_2(): pass
        def test_b_3(): pass
        def test_b_4(): pass
    """)

    tests_run = []
    for test_group in range(1, 5):
        result = testdir.inline_run('--test-group-count', '4',
                                    '--test-group', str(test_group),
                                    '--test-group-random-seed', '5',
                                    "-k", "test_a")
        group_1 = [x.item.name for x in result.calls if x._name == 'pytest_runtest_call']
        result.assertoutcome(passed=1)
        tests_run += group_1

    tests_run.sort()
    assert tests_run == [
        "test_a_1",
        "test_a_2",
        "test_a_3",
        "test_a_4",
    ]


def test_group_runs_all_test(testdir):
    """Given a large set of tests executed in random order, assert that all
    tests are executed.
    """
    testdir.makepyfile("""
        def test_b(): pass
        def test_c(): pass
        def test_d(): pass
        def test_e(): pass
        def test_f(): pass
        def test_g(): pass
        def test_h(): pass
        def test_i(): pass
        def test_j(): pass
        def test_k(): pass
        def test_l(): pass
        def test_m(): pass
        def test_n(): pass
        def test_o(): pass
        def test_p(): pass
        def test_q(): pass
        def test_r(): pass
        def test_s(): pass
        def test_t(): pass
        def test_u(): pass
        def test_v(): pass
        def test_w(): pass
        def test_x(): pass
        def test_y(): pass
        def test_z(): pass
    """)

    result = testdir.inline_run('--test-group-count', '2',
                                '--test-group', '1',
                                '--test-group-random-seed', '5')
    group_1 = [x.item.name for x in result.calls if x._name == 'pytest_runtest_call']
    result.assertoutcome(passed=13)

    result = testdir.inline_run('--test-group-count', '2',
                                '--test-group', '2',
                                '--test-group-random-seed', '5')
    group_2 = [x.item.name for x in result.calls if x._name == 'pytest_runtest_call']
    result.assertoutcome(passed=12)

    result = testdir.inline_run('--test-group-count', '1',
                                '--test-group', '1',
                                '--test-group-random-seed', '5')
    all_tests = [x.item.name for x in result.calls if x._name == 'pytest_runtest_call']

    assert set(group_1 + group_2) == set(all_tests)
