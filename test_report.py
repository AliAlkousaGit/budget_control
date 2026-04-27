def test_get_data():
    from budget_control.report.budget_control_summary.budget_control_summary import get_data
    data = get_data({})
    print('Number of rows:', len(data))
    if data:
        print('Columns:', list(data[0].keys()))
        print('First row:', data[0])
    else:
        print('No data')

test_get_data()