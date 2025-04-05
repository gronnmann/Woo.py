from woo_py.models.report import SalesReport, TopSellersReport
from woo_py.woo import Woo


def test_reports_methods(woo: Woo):
    # Test sales report endpoint
    sales_report = woo.get_sales_report()
    # We can't guarantee there will be sales data, but we can check the response type
    assert sales_report is None or isinstance(sales_report, SalesReport)
    
    # Test top sellers report endpoint
    top_sellers = woo.get_top_sellers_report()
    # We can verify we get a list, but it may be empty if no sales
    assert isinstance(top_sellers, list)
    for seller in top_sellers:
        assert isinstance(seller, TopSellersReport)