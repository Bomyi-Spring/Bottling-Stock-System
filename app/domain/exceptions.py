class DomainException(Exception):
    """도메인 계층 최상위 기본 예외 클래스"""
    pass


# ==========================================
# 1. 원자재(Material) 관련 예외
# ==========================================

class MaterialNotFoundException(DomainException):
    """원자재를 찾을 수 없을 때 발생"""
    def __init__(self, material_id: int):
        self.material_id = material_id
        super().__init__(f"ID가 {material_id}인 원자재를 찾을 수 없습니다.")


class InsufficientStockException(DomainException):
    """재고가 부족할 때 발생"""
    def __init__(self, target_name: str, current_stock: float, required_stock: float):
        self.target_name = target_name
        self.current_stock = current_stock
        self.required_stock = required_stock
        super().__init__(
            f"'{target_name}'의 재고가 부족합니다. (현재 재고: {current_stock}, 필요 수량: {required_stock})"
        )


# ==========================================
# 2. 완제품(Product) 관련 예외
# ==========================================

class ProductNotFoundException(DomainException):
    """완제품을 찾을 수 없을 때 발생"""
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"ID가 {product_id}인 완제품을 찾을 수 없습니다.")


class DuplicateSKUException(DomainException):
    """이미 존재하는 SKU 코드로 등록 시도 시 발생"""
    def __init__(self, sku: str):
        self.sku = sku
        super().__init__(f"이미 존재하는 SKU 코드입니다: '{sku}'")