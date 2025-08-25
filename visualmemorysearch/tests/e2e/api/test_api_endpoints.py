#!/usr/bin/env python3
"""
API Testing Script for Visual Memory Search FastAPI Backend
Tests all endpoints and provides comprehensive documentation.
"""

import requests
import json
import time
import os
from pathlib import Path
from typing import Dict, Any, List

class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = {}
        
    def test_endpoint(self, method: str, endpoint: str, data: Any = None, 
                     expected_status: int = 200, description: str = "") -> Dict[str, Any]:
        """Test a single endpoint and return results."""
        url = f"{self.base_url}{endpoint}"
        
        print(f"\n🔍 Testing {method.upper()} {endpoint}")
        print(f"   Description: {description}")
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            success = response.status_code == expected_status
            result = {
                "method": method.upper(),
                "endpoint": endpoint,
                "url": url,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "response_size": len(response.content),
                "description": description
            }
            
            if success:
                print(f"   ✅ SUCCESS - Status: {response.status_code}")
                if response.content:
                    try:
                        response_data = response.json()
                        result["response_data"] = response_data
                        print(f"   📊 Response: {json.dumps(response_data, indent=2)[:200]}...")
                    except:
                        result["response_text"] = response.text[:200]
                        print(f"   📄 Response: {response.text[:200]}...")
            else:
                print(f"   ❌ FAILED - Expected: {expected_status}, Got: {response.status_code}")
                if response.content:
                    try:
                        error_data = response.json()
                        result["error_data"] = error_data
                        print(f"   🚨 Error: {json.dumps(error_data, indent=2)}")
                    except:
                        result["error_text"] = response.text
                        print(f"   🚨 Error: {response.text}")
            
            return result
            
        except Exception as e:
            error_result = {
                "method": method.upper(),
                "endpoint": endpoint,
                "url": url,
                "status_code": None,
                "expected_status": expected_status,
                "success": False,
                "error": str(e),
                "description": description
            }
            print(f"   💥 EXCEPTION: {str(e)}")
            return error_result
    
    def test_health_endpoint(self):
        """Test the health check endpoint."""
        return self.test_endpoint(
            "GET", "/api/health",
            expected_status=200,
            description="Health check endpoint to verify service status"
        )
    
    def test_list_screenshots(self):
        """Test the list screenshots endpoint."""
        return self.test_endpoint(
            "GET", "/api/screenshots",
            expected_status=200,
            description="Get list of all indexed screenshots"
        )
    
    def test_search_screenshots(self):
        """Test the search screenshots endpoint."""
        search_queries = [
            {"query": "test", "search_type": "combined", "max_results": 5},
            {"query": "screenshot", "search_type": "text", "max_results": 3},
            {"query": "image", "search_type": "visual", "max_results": 2}
        ]
        
        results = []
        for query in search_queries:
            result = self.test_endpoint(
                "POST", "/api/search",
                data=query,
                expected_status=200,
                description=f"Search with query: {query['query']} (type: {query['search_type']})"
            )
            results.append(result)
        
        return results
    
    def test_upload_screenshot(self):
        """Test the upload screenshot endpoint."""
        # Create a test image file
        test_image_path = Path("test_image.png")
        if not test_image_path.exists():
            # Create a simple test image using PIL if available
            try:
                from PIL import Image, ImageDraw
                img = Image.new('RGB', (100, 100), color='red')
                draw = ImageDraw.Draw(img)
                draw.text((10, 40), "TEST", fill='white')
                img.save(test_image_path)
                print(f"   📸 Created test image: {test_image_path}")
            except ImportError:
                print("   ⚠️  PIL not available, skipping upload test")
                return None
        
        # Test file upload
        try:
            with open(test_image_path, 'rb') as f:
                files = {'file': ('test_image.png', f, 'image/png')}
                response = self.session.post(f"{self.base_url}/api/upload", files=files)
            
            success = response.status_code == 200
            result = {
                "method": "POST",
                "endpoint": "/api/upload",
                "url": f"{self.base_url}/api/upload",
                "status_code": response.status_code,
                "expected_status": 200,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "response_size": len(response.content),
                "description": "Upload a test screenshot file"
            }
            
            if success:
                print(f"   ✅ UPLOAD SUCCESS - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    result["response_data"] = response_data
                    print(f"   📊 Response: {json.dumps(response_data, indent=2)}")
                except:
                    result["response_text"] = response.text
                    print(f"   📄 Response: {response.text}")
            else:
                print(f"   ❌ UPLOAD FAILED - Expected: 200, Got: {response.status_code}")
                if response.content:
                    try:
                        error_data = response.json()
                        result["error_data"] = error_data
                        print(f"   🚨 Error: {json.dumps(error_data, indent=2)}")
                    except:
                        result["error_text"] = response.text
                        print(f"   🚨 Error: {response.text}")
            
            return result
            
        except Exception as e:
            error_result = {
                "method": "POST",
                "endpoint": "/api/upload",
                "url": f"{self.base_url}/api/upload",
                "status_code": None,
                "expected_status": 200,
                "success": False,
                "error": str(e),
                "description": "Upload a test screenshot file"
            }
            print(f"   💥 UPLOAD EXCEPTION: {str(e)}")
            return error_result
    
    def test_admin_endpoints(self):
        """Test all admin endpoints."""
        results = []
        
        # Test admin status
        results.append(self.test_endpoint(
            "GET", "/api/admin/status",
            expected_status=200,
            description="Get system status and statistics"
        ))
        
        # Test rebuild index
        results.append(self.test_endpoint(
            "POST", "/api/admin/rebuild-index",
            expected_status=200,
            description="Rebuild the search index from scratch"
        ))
        
        # Test generate test data
        results.append(self.test_endpoint(
            "POST", "/api/admin/generate-test-data",
            expected_status=200,
            description="Generate test screenshot data"
        ))
        
        # Test OpenAI key validation
        results.append(self.test_endpoint(
            "POST", "/api/admin/test-openai",
            data={"api_key": "test_key"},
            expected_status=200,
            description="Test OpenAI API key validity"
        ))
        
        return results
    
    def test_screenshot_management(self):
        """Test screenshot management endpoints."""
        results = []
        
        # First, get a list of screenshots to find one to test with
        list_response = self.session.get(f"{self.base_url}/api/screenshots")
        if list_response.status_code == 200:
            screenshots = list_response.json()
            if screenshots:
                # Test getting screenshot info
                test_filename = screenshots[0]["filename"]
                results.append(self.test_endpoint(
                    "GET", f"/api/screenshot/{test_filename}",
                    expected_status=200,
                    description=f"Get info for screenshot: {test_filename}"
                ))
                
                # Test serving screenshot image
                results.append(self.test_endpoint(
                    "GET", f"/api/screenshots/{test_filename}",
                    expected_status=200,
                    description=f"Serve screenshot image: {test_filename}"
                ))
                
                # Test deleting screenshot (we'll skip this to avoid data loss)
                print(f"   ⚠️  Skipping DELETE test for {test_filename} to preserve data")
            else:
                print("   ⚠️  No screenshots available for testing management endpoints")
        else:
            print("   ⚠️  Could not fetch screenshots for management testing")
        
        return results
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all API tests and return comprehensive results."""
        print("🚀 Starting Comprehensive API Testing")
        print("=" * 60)
        
        start_time = time.time()
        
        # Test all endpoint categories
        self.test_results["health"] = self.test_health_endpoint()
        self.test_results["list_screenshots"] = self.test_list_screenshots()
        self.test_results["search"] = self.test_search_screenshots()
        self.test_results["upload"] = self.test_upload_screenshot()
        self.test_results["admin"] = self.test_admin_endpoints()
        self.test_results["management"] = self.test_screenshot_management()
        
        total_time = time.time() - start_time
        
        # Generate summary
        total_tests = 0
        successful_tests = 0
        
        for category, results in self.test_results.items():
            if isinstance(results, list):
                for result in results:
                    total_tests += 1
                    if result.get("success", False):
                        successful_tests += 1
            else:
                total_tests += 1
                if results.get("success", False):
                    successful_tests += 1
        
        summary = {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": total_tests - successful_tests,
            "success_rate": (successful_tests / total_tests * 100) if total_tests > 0 else 0,
            "total_time": total_time,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.test_results["summary"] = summary
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {total_tests - successful_tests}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Total Time: {total_time:.2f} seconds")
        print("=" * 60)
        
        return self.test_results
    
    def save_results(self, filename: str = "api_test_results.json"):
        """Save test results to a JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump(self.test_results, f, indent=2, default=str)
            print(f"\n💾 Test results saved to: {filename}")
        except Exception as e:
            print(f"\n❌ Failed to save results: {e}")
    
    def generate_markdown_report(self, filename: str = "API_TEST_REPORT.md"):
        """Generate a markdown report of the test results."""
        try:
            with open(filename, 'w') as f:
                f.write("# API Test Report\n\n")
                f.write(f"**Generated:** {self.test_results.get('summary', {}).get('timestamp', 'Unknown')}\n\n")
                
                # Summary
                summary = self.test_results.get('summary', {})
                f.write("## Summary\n\n")
                f.write(f"- **Total Tests:** {summary.get('total_tests', 0)}\n")
                f.write(f"- **Successful:** {summary.get('successful_tests', 0)}\n")
                f.write(f"- **Failed:** {summary.get('failed_tests', 0)}\n")
                f.write(f"- **Success Rate:** {summary.get('success_rate', 0):.1f}%\n")
                f.write(f"- **Total Time:** {summary.get('total_time', 0):.2f} seconds\n\n")
                
                # Detailed Results
                f.write("## Detailed Results\n\n")
                
                for category, results in self.test_results.items():
                    if category == "summary":
                        continue
                    
                    f.write(f"### {category.replace('_', ' ').title()}\n\n")
                    
                    if isinstance(results, list):
                        for result in results:
                            status = "✅ PASS" if result.get("success", False) else "❌ FAIL"
                            f.write(f"- **{status}** {result.get('method', '')} {result.get('endpoint', '')}\n")
                            f.write(f"  - Description: {result.get('description', 'N/A')}\n")
                            f.write(f"  - Status: {result.get('status_code', 'N/A')} (Expected: {result.get('expected_status', 'N/A')})\n")
                            f.write(f"  - Response Time: {result.get('response_time', 'N/A')}s\n")
                            if result.get('error'):
                                f.write(f"  - Error: {result.get('error', 'N/A')}\n")
                            f.write("\n")
                    else:
                        status = "✅ PASS" if results.get("success", False) else "❌ FAIL"
                        f.write(f"- **{status}** {results.get('method', '')} {results.get('endpoint', '')}\n")
                        f.write(f"  - Description: {results.get('description', 'N/A')}\n")
                        f.write(f"  - Status: {results.get('status_code', 'N/A')} (Expected: {results.get('expected_status', 'N/A')})\n")
                        f.write(f"  - Response Time: {results.get('response_time', 'N/A')}s\n")
                        if results.get('error'):
                            f.write(f"  - Error: {results.get('error', 'N/A')}\n")
                        f.write("\n")
            
            print(f"📝 Markdown report generated: {filename}")
        except Exception as e:
            print(f"❌ Failed to generate markdown report: {e}")

def main():
    """Main function to run the API tests."""
    print("🔧 Visual Memory Search API Testing Tool")
    print("=" * 60)
    
    # Check if backend is running
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and accessible")
        else:
            print("⚠️  Backend responded but with unexpected status")
    except requests.exceptions.RequestException:
        print("❌ Backend is not accessible. Please start the FastAPI server first.")
        print("   Run: python run_fastapi.py")
        return
    
    # Run tests
    tester = APITester()
    results = tester.run_all_tests()
    
    # Save results
    tester.save_results()
    tester.generate_markdown_report()
    
    print("\n🎉 API testing completed!")
    print("Check the generated files for detailed results.")

if __name__ == "__main__":
    main()
