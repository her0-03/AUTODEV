from typing import Dict
import json

class AnalyticsService:
    
    def estimate_hosting_cost(self, spec: Dict) -> Dict:
        """Estimate monthly hosting costs for different providers"""
        entities = len(spec.get("database", {}).get("entities", []))
        endpoints = len(spec.get("api", {}).get("endpoints", []))
        pages = len(spec.get("ui", {}).get("pages", []))
        
        # Simple estimation based on complexity
        complexity_score = (entities * 2) + endpoints + (pages * 0.5)
        
        aws_cost = max(20, complexity_score * 5)
        gcp_cost = max(18, complexity_score * 4.5)
        azure_cost = max(22, complexity_score * 5.2)
        vercel_cost = max(0, (pages * 2))
        
        return {
            "aws": {
                "monthly": round(aws_cost, 2),
                "breakdown": {
                    "ec2": round(aws_cost * 0.4, 2),
                    "rds": round(aws_cost * 0.3, 2),
                    "s3": round(aws_cost * 0.1, 2),
                    "cloudfront": round(aws_cost * 0.2, 2)
                }
            },
            "gcp": {
                "monthly": round(gcp_cost, 2),
                "breakdown": {
                    "compute_engine": round(gcp_cost * 0.4, 2),
                    "cloud_sql": round(gcp_cost * 0.3, 2),
                    "cloud_storage": round(gcp_cost * 0.3, 2)
                }
            },
            "azure": {
                "monthly": round(azure_cost, 2),
                "breakdown": {
                    "app_service": round(azure_cost * 0.5, 2),
                    "sql_database": round(azure_cost * 0.3, 2),
                    "blob_storage": round(azure_cost * 0.2, 2)
                }
            },
            "vercel": {
                "monthly": round(vercel_cost, 2),
                "note": "Frontend only, backend needs separate hosting"
            }
        }
    
    def predict_performance(self, spec: Dict) -> Dict:
        """Predict application performance metrics"""
        entities = len(spec.get("database", {}).get("entities", []))
        endpoints = len(spec.get("api", {}).get("endpoints", []))
        
        # Estimate based on complexity
        avg_response_time = 50 + (entities * 10) + (endpoints * 5)
        requests_per_second = max(100, 1000 - (entities * 50))
        
        return {
            "response_time": {
                "average_ms": avg_response_time,
                "p95_ms": avg_response_time * 2,
                "p99_ms": avg_response_time * 3
            },
            "throughput": {
                "requests_per_second": requests_per_second,
                "concurrent_users": requests_per_second * 10
            },
            "database": {
                "query_time_ms": 10 + (entities * 2),
                "connection_pool": 20
            },
            "recommendations": [
                "Add Redis caching for frequently accessed data",
                "Implement database indexing on foreign keys",
                "Use CDN for static assets"
            ]
        }
    
    def analyze_scalability(self, spec: Dict) -> Dict:
        """Analyze scalability potential"""
        entities = len(spec.get("database", {}).get("entities", []))
        endpoints = len(spec.get("api", {}).get("endpoints", []))
        
        # Calculate scalability score
        has_caching = False  # Could be detected from spec
        has_async = True  # FastAPI is async by default
        
        score = 70
        if has_caching:
            score += 10
        if has_async:
            score += 10
        if entities < 10:
            score += 10
        
        return {
            "score": min(100, score),
            "rating": "Excellent" if score >= 80 else "Good" if score >= 60 else "Fair",
            "bottlenecks": [
                {"component": "Database", "severity": "medium", "solution": "Add read replicas"},
                {"component": "API", "severity": "low", "solution": "Implement rate limiting"}
            ],
            "scaling_strategy": {
                "horizontal": {
                    "feasible": True,
                    "max_instances": 10,
                    "load_balancer": "Required"
                },
                "vertical": {
                    "current": "2 vCPU, 4GB RAM",
                    "recommended": "4 vCPU, 8GB RAM for production"
                }
            },
            "capacity": {
                "current_users": 1000,
                "max_users_without_scaling": 5000,
                "with_scaling": 50000
            }
        }
    
    def calculate_security_score(self, spec: Dict, security_analysis: Dict) -> Dict:
        """Calculate overall security score"""
        base_score = security_analysis.get("score", 75)
        
        # Adjust based on features
        has_auth = any("auth" in e.get("path", "").lower() for e in spec.get("api", {}).get("endpoints", []))
        has_https = True  # Assumed in modern deployments
        
        if has_auth:
            base_score += 5
        if has_https:
            base_score += 5
        
        return {
            "overall_score": min(100, base_score),
            "grade": "A" if base_score >= 90 else "B" if base_score >= 75 else "C",
            "vulnerabilities": security_analysis.get("issues", []),
            "compliance": {
                "gdpr": has_auth,
                "owasp": base_score >= 70,
                "pci_dss": False  # Requires payment handling
            },
            "recommendations": security_analysis.get("recommendations", [])
        }
