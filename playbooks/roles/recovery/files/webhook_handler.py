from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Handle webhook requests from Alertmanager and replace containers.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid payload"}), 400

    alerts = data.get("alerts", [])
    for alert in alerts:

        container_name = alert.get("labels", {}).get("container", "nginx_default")

        print(f"Received alert for container: {container_name}")

        remove_container_if_exists(container_name)

        new_container_name = f"{container_name}_replacement"
        create_nginx_container(new_container_name)

    return jsonify({"message": "Containers processed successfully"}), 200


def remove_container_if_exists(container_name):
    """
    Stop and remove a Docker container if it exists.
    """
    try:
        subprocess.run(
            f"docker rm -f {container_name}",
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(f"Removed container: {container_name}")
    except subprocess.CalledProcessError:
        print(f"No existing container named {container_name} found.")


def create_nginx_container(container_name):
    """
    Create a new NGINX container with the given name.
    """
    try:
        subprocess.run(
            f"docker run -d --name {container_name} nginx",
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(f"Created new container: {container_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create container {container_name}: {e}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

