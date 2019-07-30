import requests


def test_list_clusters(populated_cluster):
    url = populated_cluster["url"].rstrip("/")
    response = requests.get(f"{url}/clusters")
    response.raise_for_status()
    assert "/clusters/local" in response.text


def test_list_cluster_resource_type_not_found(populated_cluster):
    url = populated_cluster["url"].rstrip("/")
    response = requests.get(f"{url}/clusters/local/foobars")
    assert response.status_code == 404
    assert "Resource type not found" in response.text


def test_list_cluster_resources(populated_cluster):
    url = populated_cluster["url"].rstrip("/")
    response = requests.get(f"{url}/clusters/local/nodes")
    response.raise_for_status()
    assert "/clusters/local/nodes/kube-web-view-e2e-control-plane" in response.text


def test_list_namespaced_resources(populated_cluster):
    url = populated_cluster["url"].rstrip("/")
    response = requests.get(f"{url}/clusters/local/namespaces/default/deployments")
    response.raise_for_status()
    assert "application=kube-web-view" in response.text
    assert "kube-web-view-container" in response.text


def test_list_multple_namespaced_resources(populated_cluster):
    url = populated_cluster["url"].rstrip("/")
    response = requests.get(
        f"{url}/clusters/local/namespaces/default/deployments,services"
    )
    response.raise_for_status()
    assert "application=kube-web-view" in response.text
    assert "kube-web-view-container" in response.text
    assert "ClusterIP" in response.text


def test_download_tsv(populated_cluster):
    url = populated_cluster["url"].rstrip("/")
    response = requests.get(
        f"{url}/clusters/local/namespaces/default/deployments?download=tsv"
    )
    response.raise_for_status()
    lines = response.text.split("\n")
    assert lines[0].startswith("Namespace")
    assert lines[1].startswith("default\tkube-web-view")


def test_list_resources_in_all_namespaces(populated_cluster):
    url = populated_cluster["url"].rstrip("/")
    response = requests.get(f"{url}/clusters/local/namespaces/_all/deployments")
    response.raise_for_status()
    assert "application=kube-web-view" in response.text
    # deployments in kube-system are also listed:
    assert "/namespaces/kube-system/deployments/coredns" in response.text


def test_list_pods_wrong_container_image(populated_cluster):
    url = populated_cluster["url"].rstrip("/")
    response = requests.get(
        f"{url}/clusters/local/namespaces/default/pods?selector=e2e=wrong-container-image"
    )
    response.raise_for_status()
    assert "ImagePullBackOff" in response.text
    assert "has-text-danger" in response.text
