# 🤖 ChatGPT 2026 Integration: Official Plugins & MCP Server Guide

Connect the **Wall Street Hedge Fund Suite** directly into ChatGPT (Agent Plugins 1.0 & Remote MCP Server).
Executes serverless institutional quant calculations via remote MCP and OAuth 2.1 with zero local setup.

---

## 💡 ChatGPT 2026 UI Architecture (이해하기)

ChatGPT 2026 환경은 플러그인과 MCP 서버가 **2단계 분리 구조**로 동작합니다:

1. **플러그인 레이어 (`맞춤 설정 > 플러그인`)**:
   - 플러그인의 메타데이터(`plugin.json`), 스킬 정의(`SKILL.md`), 그리고 필요한 MCP 서버의 의존성을 관리합니다.
   - 대화창에서 `@Wall Street Hedge Fund Suite`로 플러그인을 호출하고 스킬을 활성화하는 역할을 합니다.
2. **MCP 서버 레이어 (`설정 > MCP 서버`)**:
   - 실제 도구(`tools/list`, `tools/call`)를 실행하기 위한 **실시간 통신 파이프라인 및 인증(OAuth / Bearer)**을 관리합니다.
   - **헤더 설정 여부**에 따라 제3자 일반 유저용(OAuth 인증 버튼)과 개발자 개인 테스트용(Direct Bearer)으로 나뉩니다.

---

## ⚡ Method 1: Official 2026 ChatGPT Plugin (OAuth 2.1 Gateway) — 추천 표준

이 방식은 전 세계 사용자가 각자의 Apify 계정(무료 티어: 월 $5 무료 크레딧 = 약 625회 무료 쿼리)으로 안전하게 인증하며, 쿼리 발생 시 플랫폼 제작자에게 80% 정산 수익(PPE)이 발생하는 완전 상용화 구조입니다.

### 📍 1단계: MCP 서버 연결 (`설정 > MCP 서버`)

1. ChatGPT 좌측 하단 프로필 → **[설정 (Settings)]** → **[MCP 서버]** 탭으로 이동합니다.
2. 우측 상단의 **[+ 서버 추가]** 버튼을 클릭합니다.
3. 다음과 같이 입력합니다:
   - **URL**: `https://wallstreet.mcp-collector.workers.dev`
   - **기본 token 환경 변수**: 비워두거나 기본값(`MCP_BEARER_TOKEN`) 유지
   - **헤더 (Headers)**: **★반드시 비워둡니다 (헤더 추가 안 함)**
     > ⚠️ **주의 (헤더를 비워두는 이유)**:
     > - **헤더를 비워두면**: ChatGPT가 게이트웨이의 OAuth 2.1 메타데이터(`RFC 8414/9728`)를 자동 감지하여, 대화창에 사용자별 **[인증(Authenticate)]** 버튼을 띄웁니다. 사용자는 각자의 토큰으로 로그인하므로 제작자의 크레딧이 소모되지 않습니다.
     > - **헤더에 본인 토큰(`Bearer apify_api_...`)을 넣으면**: OAuth를 건너뛰고 해당 고정 토큰으로 직통 연결되므로, 개발자 로컬 테스트용으로만 사용해야 합니다.
4. **[저장]** 버튼을 클릭합니다.

---

### 📍 2단계: 플러그인 확인 및 스킬 활성화 (`맞춤 설정 > 플러그인`)

1. 좌측 메뉴 상단 **[맞춤 설정]** → **[플러그인]**으로 이동합니다.
2. 설치된 목록에서 **`Wall Street Hedge Fund Suite`**를 클릭합니다.
3. 내부 정보 확인:
   - **버전**: `0.1.4`
   - **MCP 서버 1**: `Wallstreet-suite`
   - **스킬 1**: `institutional-equity-analysis`
4. 스킬 토글 스위치가 **활성화(ON - 파란색)** 되어 있는지 확인합니다.

---

### 📍 3단계: 대화창에서 360° 퀀트 분석 실행 & OAuth 인증

1. ChatGPT 새 대화창으로 이동합니다.
2. 다음과 같이 입력하고 전송합니다:
   ```text
   @Wall Street Hedge Fund Suite Run a full 360-degree institutional quant analysis on NVDA.
   ```
3. **[인증 (Authenticate)]** 버튼이 나타나면 클릭합니다:
   - Cloudflare Workers OAuth 2.1 보안 승인 카드(`https://wallstreet.mcp-collector.workers.dev/oauth/authorize`)가 열립니다.
   - 사용자의 개인 Apify API Token을 입력하고 **[Authorize]**를 클릭합니다.
   - *(토큰은 서버에 영구 저장되지 않으며, AES-GCM으로 안전하게 암호화되어 세션 동안만 유지됩니다.)*
4. 인증 즉시 ChatGPT가 실시간 60종 퀀트 엔진을 호출하여 **피오트로스키 F-Score, 알트만 Z-Score, 버핏 경제적 해자(ROIC vs WACC), RSI, VIX 백워데이션, 그레이엄 내재가치**가 포함된 전문 헤지펀드 투자 메모를 출력합니다.

---

## 🛠️ 트러블슈팅 & 자주 묻는 질문 (FAQ)

### Q1. 대화창에서 *"analysis tools aren't available in this session / Please reconnect"* 메시지가 뜹니다.
- **원인**: ChatGPT 세션에서 MCP 서버의 연결 캐시가 일시적으로 만료되었거나, 인증 토큰이 갱신되지 않았을 때 발생합니다.
- **해결법**:
  1. `설정 > MCP 서버`로 이동하여 `wall_street_hedge_fund_suite` 토글을 껐다가 다시 켭니다.
  2. 만약 헤더에 잘못된 값이 들어가 있다면 헤더를 휴지통 아이콘을 눌러 모두 삭제하고 **[저장]**을 누릅니다.
  3. 대화창을 새로고침하고 다시 프롬프트를 전송하면 나타나는 **[인증]** 버튼을 눌러 1회 재인증하면 정상 작동합니다.

### Q2. 내가 헤더에 내 Apify 토큰을 넣으면 다른 사용자들도 내 토큰/크레딧을 쓰게 되나요?
- **아닙니다!**:
  - `설정 > MCP 서버`의 헤더는 **본인 브라우저 세션에만 적용되는 로컬 설정**입니다.
  - 하지만 공개 배포 규격에서는 헤더를 비워두는 것이 표준입니다. 헤더를 비워두어야 접속하는 모든 유저가 본인의 Apify 계정(무료 $5 포함)으로 OAuth 인증을 진행하게 되며, 유저가 유료 쿼리를 실행할 때마다 제작자(`mcp_collector`)에게 80% 순수익이 정산됩니다.

---

## 🏛️ Method 2: Custom GPT Actions (OpenAPI 3.0 레거시)

레거시 Custom GPT 환경을 유지하고자 하는 경우:
1. **[ChatGPT](https://chatgpt.com)** → **Explore GPTs** → **+ Create**로 이동합니다.
2. **Instructions**: [`custom-gpt-instructions.md`](custom-gpt-instructions.md)의 시스템 프롬프트를 복사하여 붙여넣습니다.
3. **Actions**: [`openapi-actions-schema.yaml`](openapi-actions-schema.yaml)의 스키마를 가져옵니다.
4. 공개 범위를 **Everyone** 또는 **Anyone with a link**로 설정하고 배포합니다.
