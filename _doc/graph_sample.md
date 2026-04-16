# Mermaid Graph Samples (Ultimate Guide)

이 문서는 Mermaid Flowchart의 4가지 방향 패턴과 주요 기능을 모두 포함한 샘플입니다.

---

## 1. Top Down (TD): 수직 구조 & 서브그래프
복잡한 시스템의 영역을 나누거나 수직적인 흐름을 표현할 때 최적입니다.

```mermaid
graph TD
    %% 서브그래프 정의
    subgraph 클라이언트_영역 [프론트엔드]
        A([시작포인트]) --> B[/데이터 입력/]
        B --> C["줄바꿈 포함<br/>일반 프로세스"]
    end

    subgraph 서버_영역 [백엔드]
        C --> D{의사결정}
        D -- 예 --> E[[서브루틴 실행]]
        D -- 아니오 --> F[(데이터베이스)]
    end

    %% 특수 도형
    E --> G((종료))
    F -.-> G

    %% 스타일링
    style 클라이언트_영역 fill:#f9f,stroke:#333,stroke-width:2px
    style 서버_영역 fill:#bbf,stroke:#333,stroke-width:2px
    style G fill:#f66,stroke:#333,stroke-weight:4px
```

---

## 2. Left Right (LR): 수평 구조 & 다양한 연결선
시간의 흐름이나 긴 작업 공정을 표현할 때 가로 폭을 효율적으로 사용합니다.

```mermaid
flowchart LR
    %% 다양한 화살표 종류
    Node1[일반 연결] --> Node2[화살표]
    Node2 --- Node3[선만 있음]
    Node3 -- 텍스트 포함 --- Node4[설명]
    Node4 == 두꺼운 선 ==> Node5{중요}
    Node5 -- "실선 화살표" --> Node6((A))
    Node5 -. 점선 .-> Node7((B))
    Node5 --x X연결
    Node5 --o O연결

    %% 노드 모양
    Node6([둥근 캡슐])
    Node7{{육각형}}
```

---

## 3. Bottom Top (BT): 상향식 & 스타일 클래스
역방향 계층 구조나 아래에서 위로 쌓아 올리는 구조를 표현합니다.

```mermaid
graph BT
    %% 클래스 정의
    classDef hlight fill:#ffde5e,stroke:#333,stroke-width:2px,color:#000
    classDef danger fill:#ff6347,stroke:#333,color:#fff

    Base[기반 기술] --> App[애플리케이션]
    App --> Service[서비스 계층]
    Service --> UX[사용자 경험]

    %% 클래스 적용
    class Base hlight
    class UX danger
```

---

## 4. Right Left (RL): 우측 시작 구조
오른쪽에서 왼쪽으로 진행되는 특수한 사례에 사용됩니다.

```mermaid
flowchart RL
    Start((시작)) --> Step1[1단계]
    Step1 --> Step2{2단계 확인}
    Step2 -- 통과 --> End([최종 목적지])
    
    %% 멀티 노드 연결
    Step2 -- 반려 --> Step1
    
    %% 영역 표시
    subgraph 검토_루프
        Step1
        Step2
    end
```

---

## 💡 주요 팁
| 기능 | 예시 | 설명 |
| :--- | :--- | :--- |
| **텍스트 줄바꿈** | `"<br/>"` | 노드 안에서 줄바꿈 시 사용 |
| **도형 종류** | `[]`, `()`, `{}` 등 | 사각형, 원형, 다이아몬드 등 다양한 모양 지원 |
| **선 스타일** | `-->`, `-.->`, `==>` | 실선, 점선, 굵은 선 등 표현 가능 |
| **스타일링** | `style` 또는 `classDef` | 특정 노드나 그룹의 색상, 선 굵기 등 커스텀 가능 |
