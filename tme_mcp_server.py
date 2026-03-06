import logging
from urllib.parse import quote

from mcp_app import mcp
from tme_auth import _make_request, TME_COUNTRY, TME_CURRENCY

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

logger.info("=== STARTING TME MCP SERVER ===")

# Tools are registered at import time via @mcp.tool() decorators below.

# ---------------------------------------------------------------------------
# Search & Browse
# ---------------------------------------------------------------------------


@mcp.tool()
def search_products(
    search: str,
    page: int = 1,
    limit: int = 20,
    category_id: str | None = None,
    with_stock: bool = False,
) -> dict:
    """Search TME products by keyword or part number.

    Args:
        search: Search phrase or part number
        page: Page number (default: 1)
        limit: Results per page, max 200 (default: 20)
        category_id: Optional category ID filter
        with_stock: Only return products that are in stock (default: False)
    """
    params = {"SearchPlain": search, "SearchPage": page, "Limit": limit}
    if with_stock:
        params["SearchWithStock"] = "true"
    if category_id:
        params["SearchCategory"] = category_id
    return _make_request("Products/Search", params)


@mcp.tool()
def autocomplete(phrase: str) -> dict:
    """Get type-ahead suggestions for a search phrase.

    Args:
        phrase: Partial search string
    """
    return _make_request("Products/Autocomplete", {"Phrase": phrase})


@mcp.tool()
def get_categories(category_id: str | None = None) -> dict:
    """Get the TME product category tree.

    Args:
        category_id: Parent category ID to get children of. Omit for top-level categories.
    """
    params = {}
    if category_id:
        params["CategoryId"] = category_id
    # Tree=true returns nested subcategories
    params["Tree"] = "true"
    return _make_request("Products/GetCategories", params)


@mcp.tool()
def search_parameters(category_id: str) -> dict:
    """Get available filter parameters for a category.

    Args:
        category_id: Category ID to get filter parameters for
    """
    return _make_request("Products/SearchParameters", {"CategoryId": category_id})


# ---------------------------------------------------------------------------
# Product Details
# ---------------------------------------------------------------------------


@mcp.tool()
def get_products(symbols: list[str]) -> dict:
    """Get full product details for up to 50 TME product symbols.

    Args:
        symbols: List of TME product symbols (max 50)
    """
    params = {f"SymbolList[{i}]": s for i, s in enumerate(symbols[:50])}
    return _make_request("Products/GetProducts", params)


@mcp.tool()
def get_parameters(symbols: list[str]) -> dict:
    """Get technical specifications/attributes for up to 50 products.

    Args:
        symbols: List of TME product symbols (max 50)
    """
    params = {f"SymbolList[{i}]": s for i, s in enumerate(symbols[:50])}
    return _make_request("Products/GetParameters", params)


@mcp.tool()
def get_product_files(symbols: list[str]) -> dict:
    """Get datasheets, photos, and other files for up to 50 products.

    Args:
        symbols: List of TME product symbols (max 50)
    """
    params = {f"SymbolList[{i}]": s for i, s in enumerate(symbols[:50])}
    return _make_request("Products/GetProductsFiles", params)


@mcp.tool()
def get_similar_products(symbol: str) -> dict:
    """Get similar/alternative products for a given part.

    Args:
        symbol: TME product symbol
    """
    return _make_request("Products/GetSimilarProducts", {"Symbol": symbol})


# ---------------------------------------------------------------------------
# Pricing & Stock
# ---------------------------------------------------------------------------


@mcp.tool()
def get_prices(symbols: list[str]) -> dict:
    """Get pricing for up to 50 products.

    Prices returned in the configured currency (default: {currency}).

    Args:
        symbols: List of TME product symbols (max 50)
    """.format(currency=TME_CURRENCY)
    params = {f"SymbolList[{i}]": s for i, s in enumerate(symbols[:50])}
    params["Currency"] = TME_CURRENCY
    return _make_request("Products/GetPrices", params)


@mcp.tool()
def get_stocks(symbols: list[str]) -> dict:
    """Get stock/inventory levels for up to 50 products.

    Args:
        symbols: List of TME product symbols (max 50)
    """
    params = {f"SymbolList[{i}]": s for i, s in enumerate(symbols[:50])}
    return _make_request("Products/GetStocks", params)


@mcp.tool()
def get_prices_and_stocks(symbols: list[str]) -> dict:
    """Get combined pricing and stock for up to 50 products.

    Prices returned in the configured currency (default: {currency}).

    Args:
        symbols: List of TME product symbols (max 50)
    """.format(currency=TME_CURRENCY)
    params = {f"SymbolList[{i}]": s for i, s in enumerate(symbols[:50])}
    params["Currency"] = TME_CURRENCY
    return _make_request("Products/GetPricesAndStocks", params)


# ---------------------------------------------------------------------------
# Other
# ---------------------------------------------------------------------------


@mcp.tool()
def get_delivery_time(symbols: list[str], amounts: list[int] | None = None) -> dict:
    """Get estimated delivery time for up to 50 products.

    Args:
        symbols: List of TME product symbols (max 50)
        amounts: Quantity per symbol (defaults to 1 each if omitted)
    """
    symbols = symbols[:50]
    if amounts is None:
        amounts = [1] * len(symbols)
    elif len(amounts) < len(symbols):
        amounts = amounts + [1] * (len(symbols) - len(amounts))
    params = {f"SymbolList[{i}]": s for i, s in enumerate(symbols)}
    params.update({f"AmountList[{i}]": str(a) for i, a in enumerate(amounts[:len(symbols)])})
    return _make_request("Products/GetDeliveryTime", params)


@mcp.tool()
def generate_tme_url(symbol: str) -> str:
    """Generate a TME product page URL.

    Args:
        symbol: TME product symbol
    """
    country = TME_COUNTRY.lower()
    return f"https://www.tme.eu/{country}/en/details/{quote(symbol)}/"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


logger.info("=== SERVER READY ===")


def main():
    mcp.run()


if __name__ == "__main__":
    main()
