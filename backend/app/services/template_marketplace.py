from typing import Dict, List

class TemplateMarketplace:
    
    @staticmethod
    def get_templates() -> List[Dict]:
        """Get all available templates"""
        return [
            {
                "id": "ecommerce",
                "name": "E-Commerce Platform",
                "description": "Full-featured online store with cart, payments, and admin",
                "category": "E-commerce",
                "features": ["Product catalog", "Shopping cart", "Stripe integration", "Admin dashboard", "Order tracking"],
                "tech": ["FastAPI", "React", "PostgreSQL", "Redis"]
            },
            {
                "id": "saas-starter",
                "name": "SaaS Starter Kit",
                "description": "Multi-tenant SaaS with subscriptions and billing",
                "category": "SaaS",
                "features": ["User authentication", "Subscription management", "Billing", "Multi-tenancy", "Analytics"],
                "tech": ["FastAPI", "Next.js", "PostgreSQL", "Stripe"]
            },
            {
                "id": "crm",
                "name": "CRM System",
                "description": "Customer relationship management platform",
                "category": "Business",
                "features": ["Contact management", "Pipeline tracking", "Email integration", "Reports", "Tasks"],
                "tech": ["FastAPI", "Vue.js", "PostgreSQL"]
            },
            {
                "id": "web3-dapp",
                "name": "Web3 DApp",
                "description": "Decentralized application with blockchain integration",
                "category": "Blockchain",
                "features": ["Wallet connection", "Smart contracts", "NFT marketplace", "Token management"],
                "tech": ["FastAPI", "React", "Web3.js", "Solidity"]
            }
        ]
    
    @staticmethod
    def get_template_spec(template_id: str) -> Dict:
        """Get detailed specification for a template"""
        templates = {
            "ecommerce": {
                "appConfig": {
                    "name": "E-Commerce Store",
                    "description": "Modern online shopping platform",
                    "theme": "modern-blue"
                },
                "database": {
                    "entities": [
                        {
                            "name": "Product",
                            "columns": [
                                {"name": "name", "type": "string", "required": True},
                                {"name": "description", "type": "text", "required": True},
                                {"name": "price", "type": "float", "required": True},
                                {"name": "stock", "type": "integer", "required": True},
                                {"name": "image_url", "type": "string", "required": False}
                            ]
                        },
                        {
                            "name": "Order",
                            "columns": [
                                {"name": "user_id", "type": "integer", "required": True},
                                {"name": "total", "type": "float", "required": True},
                                {"name": "status", "type": "string", "required": True},
                                {"name": "payment_id", "type": "string", "required": False}
                            ]
                        },
                        {
                            "name": "Cart",
                            "columns": [
                                {"name": "user_id", "type": "integer", "required": True},
                                {"name": "product_id", "type": "integer", "required": True},
                                {"name": "quantity", "type": "integer", "required": True}
                            ]
                        }
                    ]
                },
                "api": {
                    "endpoints": [
                        {"method": "GET", "path": "/api/products", "description": "List all products"},
                        {"method": "POST", "path": "/api/products", "description": "Create product"},
                        {"method": "GET", "path": "/api/cart", "description": "Get user cart"},
                        {"method": "POST", "path": "/api/cart", "description": "Add to cart"},
                        {"method": "POST", "path": "/api/orders", "description": "Create order"},
                        {"method": "POST", "path": "/api/payments/stripe", "description": "Process payment"}
                    ]
                },
                "ui": {
                    "pages": [
                        {"route": "/", "title": "Home", "components": ["ProductGrid", "FeaturedProducts"]},
                        {"route": "/products", "title": "Products", "components": ["ProductList", "FilterSidebar"]},
                        {"route": "/cart", "title": "Shopping Cart", "components": ["CartItems", "CheckoutButton"]},
                        {"route": "/checkout", "title": "Checkout", "components": ["CheckoutForm", "OrderSummary"]},
                        {"route": "/admin", "title": "Admin Dashboard", "components": ["ProductManager", "OrderList"]}
                    ]
                }
            },
            "saas-starter": {
                "appConfig": {
                    "name": "SaaS Platform",
                    "description": "Multi-tenant SaaS application",
                    "theme": "modern-purple"
                },
                "database": {
                    "entities": [
                        {
                            "name": "Tenant",
                            "columns": [
                                {"name": "name", "type": "string", "required": True},
                                {"name": "subdomain", "type": "string", "required": True, "unique": True},
                                {"name": "plan", "type": "string", "required": True},
                                {"name": "stripe_customer_id", "type": "string", "required": False}
                            ]
                        },
                        {
                            "name": "User",
                            "columns": [
                                {"name": "email", "type": "string", "required": True, "unique": True},
                                {"name": "tenant_id", "type": "integer", "required": True},
                                {"name": "role", "type": "string", "required": True}
                            ]
                        },
                        {
                            "name": "Subscription",
                            "columns": [
                                {"name": "tenant_id", "type": "integer", "required": True},
                                {"name": "plan", "type": "string", "required": True},
                                {"name": "status", "type": "string", "required": True},
                                {"name": "stripe_subscription_id", "type": "string", "required": False}
                            ]
                        }
                    ]
                },
                "api": {
                    "endpoints": [
                        {"method": "POST", "path": "/api/tenants", "description": "Create tenant"},
                        {"method": "POST", "path": "/api/auth/register", "description": "Register user"},
                        {"method": "POST", "path": "/api/subscriptions", "description": "Create subscription"},
                        {"method": "GET", "path": "/api/analytics", "description": "Get analytics"}
                    ]
                },
                "ui": {
                    "pages": [
                        {"route": "/", "title": "Dashboard", "components": ["MetricsCards", "RecentActivity"]},
                        {"route": "/settings", "title": "Settings", "components": ["TenantSettings", "BillingInfo"]},
                        {"route": "/users", "title": "Users", "components": ["UserList", "InviteForm"]}
                    ]
                }
            }
        }
        
        return templates.get(template_id, templates["ecommerce"])
