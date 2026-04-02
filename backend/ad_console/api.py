from __future__ import annotations

import os
from dataclasses import asdict

from flask import Blueprint, jsonify, request, send_from_directory


def build_api_blueprint(services: dict[str, object], static_folder: str) -> Blueprint:
    bp = Blueprint("api", __name__)

    account_service = services["account_service"]
    password_service = services["password_service"]
    support_service = services["support_service"]
    ai_service = services["ai_service"]

    @bp.get("/api/health")
    def health() -> object:
        return jsonify({"status": "ok"})

    @bp.get("/healthcheck")
    def healthcheck() -> tuple[str, int]:
        return "", 200

    @bp.post("/api/account/request")
    def request_account() -> object:
        data = request.get_json(force=True)
        required = [data.get("username"), data.get("email"), data.get("fullName"), data.get("department")]
        if not all(required):
            return jsonify({"error": "필수 정보를 모두 입력해주세요"}), 400
        request_id = account_service.create_request(
            username=data["username"],
            email=data["email"],
            full_name=data["fullName"],
            department=data["department"],
            reason=data.get("reason", ""),
        )
        return jsonify({"message": "계정 신청이 접수되었습니다.", "requestId": request_id})

    @bp.post("/api/account/approve/<request_id>")
    def approve_account(request_id: str) -> object:
        item, temp_password = account_service.approve(request_id)
        if not item:
            return jsonify({"error": "요청을 찾을 수 없습니다"}), 404
        return jsonify({"message": "계정이 생성되었습니다", "username": item.username, "tempPassword": temp_password})

    @bp.post("/api/account/reject/<request_id>")
    def reject_account(request_id: str) -> object:
        item = account_service.reject(request_id)
        if not item:
            return jsonify({"error": "요청을 찾을 수 없습니다"}), 404
        return jsonify({"message": "계정 신청이 거부되었습니다"})

    @bp.get("/api/pending-requests")
    def pending_requests() -> object:
        items = [asdict(item) for item in account_service.list_pending()]
        return jsonify(items)

    @bp.post("/api/password/verify")
    def verify_password() -> object:
        data = request.get_json(force=True)
        if not all([data.get("username"), data.get("currentPassword")]):
            return jsonify({"error": "계정명과 비밀번호를 입력해주세요"}), 400
        if not password_service.verify_current_password(data["username"], data["currentPassword"]):
            return jsonify({"error": "현재 비밀번호가 올바르지 않습니다"}), 401
        return jsonify({"message": "인증 성공"})

    @bp.post("/api/password/change")
    def change_password() -> object:
        data = request.get_json(force=True)
        if not all([data.get("username"), data.get("currentPassword"), data.get("newPassword")]):
            return jsonify({"error": "모든 정보를 입력해주세요"}), 400
        if not password_service.change_password(data["username"], data["currentPassword"], data["newPassword"]):
            return jsonify({"error": "현재 비밀번호가 올바르지 않습니다"}), 401
        return jsonify({"message": "비밀번호가 변경되었습니다"})

    @bp.post("/api/password/send-code")
    def send_code() -> object:
        data = request.get_json(force=True)
        if not all([data.get("username"), data.get("email")]):
            return jsonify({"error": "사용자명과 이메일을 입력해주세요"}), 400
        password_service.send_reset_code(data["username"], data["email"])
        return jsonify({"message": "인증 코드가 이메일로 전송되었습니다"})

    @bp.post("/api/password/reset-with-code")
    def reset_with_code() -> object:
        data = request.get_json(force=True)
        if not all([data.get("username"), data.get("email"), data.get("code")]):
            return jsonify({"error": "모든 정보를 입력해주세요"}), 400
        temp_password = password_service.reset_with_code(data["username"], data["email"], data["code"])
        if not temp_password:
            return jsonify({"error": "인증 코드가 유효하지 않습니다"}), 400
        return jsonify({"message": "비밀번호가 초기화되었습니다", "tempPassword": temp_password})

    @bp.post("/api/password/reset-request")
    def admin_reset_password() -> object:
        data = request.get_json(force=True)
        if not all([data.get("username"), data.get("email")]):
            return jsonify({"error": "계정명과 이메일을 입력해주세요"}), 400
        temp_password = password_service.admin_reset(data["username"], data["email"])
        return jsonify({"message": "비밀번호가 초기화되었습니다", "tempPassword": temp_password})

    @bp.post("/api/qr/request")
    def qr_request() -> object:
        data = request.get_json(force=True)
        if not all([data.get("username"), data.get("email"), data.get("reason")]):
            return jsonify({"error": "모든 정보를 입력해주세요"}), 400
        support_service.request_qr_reissue(data["username"], data["email"], data["reason"])
        return jsonify({"message": "QR 코드 재생성 문의가 접수되었습니다"})

    @bp.post("/api/account/unlock-request")
    def unlock_request() -> object:
        data = request.get_json(force=True)
        if not all([data.get("username"), data.get("email"), data.get("reason")]):
            return jsonify({"error": "모든 정보를 입력해주세요"}), 400
        request_id = support_service.request_unlock(data["username"], data["email"], data["reason"])
        return jsonify({"message": "계정 잠김 해제 요청이 접수되었습니다", "requestId": request_id})

    @bp.route("/api/account/unlock-approve/<request_id>", methods=["GET", "POST"])
    def unlock_approve(request_id: str) -> tuple[str, int] | str:
        item = support_service.approve_unlock(request_id)
        if not item:
            return "<html><body><h2>이미 처리된 요청입니다.</h2></body></html>", 404
        return "<html><body><h2>승인 완료</h2><p>계정 잠금 해제가 처리되었습니다.</p></body></html>"

    @bp.route("/api/account/unlock-reject/<request_id>", methods=["GET", "POST"])
    def unlock_reject(request_id: str) -> tuple[str, int] | str:
        item = support_service.reject_unlock(request_id)
        if not item:
            return "<html><body><h2>이미 처리된 요청입니다.</h2></body></html>", 404
        return "<html><body><h2>거부 완료</h2><p>계정 잠금 해제 요청이 거부되었습니다.</p></body></html>"

    @bp.post("/api/ai/chat")
    def chat() -> object:
        data = request.get_json(force=True)
        messages = data.get("messages", [])
        if not messages:
            return jsonify({"error": "메시지가 없습니다"}), 400
        try:
            response = ai_service.chat(messages)
        except Exception as exc:
            return jsonify({"error": f"AI 응답 생성 실패: {exc}"}), 500
        return jsonify({"response": response})

    @bp.get("/")
    def index() -> object:
        return send_from_directory(static_folder, "index.html")

    @bp.get("/<path:path>")
    def spa(path: str) -> object:
        file_path = os.path.join(static_folder, path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_from_directory(static_folder, path)
        return send_from_directory(static_folder, "index.html")

    return bp
