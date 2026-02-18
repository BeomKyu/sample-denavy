AI 전용 고밀도 명세 언어(Denavy) 설계 및 컴파일러 아키텍처 리서치
1. 서론: 프롬프트 엔지니어링에서 시스템 엔지니어링으로의 전환
생성형 인공지능(Generative AI)과 대규모 언어 모델(LLM)이 단순한 텍스트 생성을 넘어 복잡한 작업을 수행하는 에이전트(Agentic AI) 시스템으로 진화함에 따라, 기존의 소프트웨어 아키텍처는 근본적인 한계에 직면하고 있다. 현재 대부분의 에이전트 시스템은 자연어 프롬프트에 의존하는 '바이브 코딩(Vibe Coding)' 방식이나, 인간 가독성에 초점을 맞춘 JSON, YAML과 같은 데이터 포맷을 그대로 사용하고 있다. 그러나 이러한 접근 방식은 확률적(Stochastic) 연산 장치인 LLM의 특성을 충분히 반영하지 못하며, 토큰 비효율성, 실행의 비결정성, 보안 취약점이라는 심각한 문제를 야기한다.
본 리서치 보고서는 이러한 문제를 해결하기 위해 고안된 AI 전용 고밀도 명세 언어인 **Denavy(Density-Native Verifiable Syntax)**의 설계 원칙과 이를 뒷받침하는 컴파일러 아키텍처를 심층 분석한다. Denavy는 인간의 의도를 기계가 이해할 수 있는 최적의 중간 표현(Intermediate Representation, IR)으로 변환하는 것을 목표로 하며, 특히 토큰 효율성을 극대화하고, 명세의 불변성을 암호학적으로 보장하며, 에이전트 격리 및 계층적 검증을 통해 실행 신뢰성을 확보하는 데 중점을 둔다.
본 연구는 700개 이상의 최신 연구 논문, 기술 문서, 벤치마크 데이터를 종합하여, 단순한 포맷 변경을 넘어선 'Compiler.next'로서의 시스템 아키텍처를 제안한다.1 이는 자연어의 모호성을 제거하고, 수학적으로 검증 가능한 실행 경로를 생성하며, 프랙탈 구조의 주소 체계를 통해 무한에 가까운 컨텍스트를 효율적으로 관리하는 차세대 AI 인프라의 청사진을 제시한다.
2. 토큰 경제학과 고밀도 구문론 (High-Density Syntax)
2.1 JSON의 한계와 토큰 인플레이션 현상
지난 수십 년간 데이터 교환의 표준으로 자리 잡은 JSON(JavaScript Object Notation)은 파서(Parser)를 위해 설계된 포맷이지, 토큰 예측기(Token Predictor)를 위해 설계된 것이 아니다. LLM은 텍스트를 바이트 페어 인코딩(BPE)과 같은 토크나이저를 통해 처리하는데, JSON의 문법적 요소인 중괄호({, }), 따옴표("), 반복되는 키(Key) 값들은 모델의 '문맥 윈도우(Context Window)'를 불필요하게 소모하는 '구문적 노이즈(Syntactic Noise)'로 작용한다.
연구 결과에 따르면, JSON의 구조적 중복성은 단순한 비용 문제를 넘어 모델의 성능 저하를 유발한다. 특히 BPE 토크나이저는 JSON의 구문 요소(예: ":{")를 여러 개의 토큰으로 분할하는 경향이 있어, 실제 정보량 대비 토큰 사용량을 급격히 증가시킨다.2 더욱 심각한 문제는 'Lost in the Middle' 현상이다. 컨텍스트의 길이가 길어질수록 모델은 중간에 위치한 정보를 인출하는 데 실패할 확률이 높아지는데 4, JSON의 낮은 정보 밀도는 이러한 위험을 가중시킨다.
2.2 TOON(Token-Oriented Object Notation) 분석과 Denavy의 설계 철학
Denavy의 구문 설계는 최근 주목받고 있는 TOON의 아키텍처에서 중요한 통찰을 얻는다. TOON은 대규모의 균일한 객체 배열(Uniform Arrays)을 처리할 때 JSON의 비효율성을 획기적으로 개선한 포맷이다.
TOON의 핵심 혁신은 '스키마 선언과 데이터의 분리'에 있다. JSON이 각 객체마다 키 값을 반복하는 것과 달리, TOON은 헤더에서 키를 한 번 선언하고, 이후 데이터는 CSV와 유사한 표 형식으로 나열한다. 벤치마크 데이터에 따르면, TOON은 포맷팅된 JSON 대비 30~60% 더 적은 토큰을 사용하면서도, 구조적 데이터 검색 정확도(Accuracy)는 69.7%에서 **73.9%**로 향상시키는 결과를 보였다.2
표 1: 데이터 포맷별 토큰 효율성 및 정확도 비교 분석
포맷 (Format)
토큰 수 (Tokens)
정확도 (Accuracy)
구조적 인식률 (Structure Awareness)
비용 효율성 점수
JSON (Pretty)
4,545 (기준)
69.7%
81.1%
15.3
YAML
3,719
69.0%
71.7%
18.6
JSON (Compact)
3,081
70.7%
88.1%
22.9
TOON
2,744
73.9%
88.0%
26.9

데이터 출처: 2 종합
위 데이터는 "토큰을 줄이면 정보 손실로 인해 정확도가 떨어질 것"이라는 직관과 상반되는 결과를 보여준다. 오히려 구문적 노이즈를 제거함으로써 모델이 의미론적 정보(Semantic Value)에 더 집중할 수 있게 되어 추론 성능이 향상됨을 시사한다. 특히 1,000 토큰당 정확도를 나타내는 비용 효율성 점수에서 TOON은 JSON 대비 76% 더 높은 효율을 기록했다.6
Denavy는 이러한 TOON의 장점을 계승하되, TOON이 가진 한계점인 '비정형 데이터 및 깊은 중첩 구조에서의 효율성 저하' 2를 극복하기 위해 하이브리드 구문을 채택한다. Denavy는 균일한 데이터 블록에는 TOON 스타일의 헤더-로(Header-Row) 압축을 적용하고, 복잡한 중첩 객체에는 YAML과 유사한 들여쓰기(Indentation) 기반의 구문을 적용하여 괄호 사용을 최소화한다.
2.3 의미론적 압축과 기호 매핑 (Symbolic Mapping)
Denavy는 단순한 공백 제거를 넘어선 '의미론적 압축(Semantic Compression)'을 수행한다. 이는 컴파일 타임에 긴 식별자나 반복되는 개념을 고밀도 기호로 매핑하는 기술이다.
예를 들어, customer_acquisition_cost라는 변수명이 코드 내에서 100번 반복된다면, LLM은 이를 매번 여러 개의 토큰으로 처리해야 한다. Denavy 컴파일러는 이를 $CAC와 같은 짧은 기호로 변환하고, 컨텍스트의 최상단(System Prompt)에 Let $CAC = customer_acquisition_cost와 같은 정의를 한 번만 삽입한다. 연구에 따르면 이러한 기호적 치환은 모델의 추론 능력에 부정적인 영향을 주지 않으면서도 전체 토큰 사용량을 획기적으로 줄일 수 있다.8 이는 프로그래밍 언어의 컴파일러가 긴 변수명을 메모리 주소로 변환하는 것과 유사한 원리다.
3. 프랙탈 구조와 재귀적 주소 체계 (Recursive Addressing)
3.1 언어의 프랙탈 기하학 (Fractal Geometry of Language)
Denavy의 주소 체계는 자연어의 본질적인 구조적 특성인 **프랙탈 기하학(Fractal Geometry)**에 기반한다. 최신 연구들은 자연어가 자기유사성(Self-similarity)과 장기 의존성(Long-range dependence, LRD)을 가지며, 허스트 지수(Hurst Parameter)가 약 0.70인 프랙탈 구조를 띤다는 것을 입증했다.9 이는 단어 수준, 문장 수준, 문단 수준, 문서 수준에서 나타나는 정보의 패턴이 통계적으로 유사함을 의미한다.
기존의 선형적 주소 체계나 절대 경로 방식은 이러한 언어의 다층적 구조를 반영하지 못한다. 반면, Denavy는 프랙탈 구조를 반영한 재귀적 주소 지정(Recursive Addressing) 방식을 도입하여, 모델이 로컬 컨텍스트와 글로벌 컨텍스트 사이를 효율적으로 오갈 수 있도록 지원한다.
3.2 상대적 주소 구문 (Relative Addressing Syntax)
Denavy는 계층적 데이터 구조 내에서 현재 위치를 기준으로 다른 데이터에 접근할 수 있는 상대 경로 문법을 제공한다. 이는 파일 시스템의 경로 탐색이나 객체 지향 언어의 this, super 개념을 프롬프트 엔지니어링에 적용한 것이다.
자기 참조 (.): 현재 활성화된 객체나 태스크 컨텍스트를 지칭한다.
부모 참조 (^. 또는 ..): 계층 구조에서 상위 레벨로 이동한다. 예를 들어, ^.output은 상위 태스크의 결과를 의미한다.12
루트 참조 (~): 전체 명세의 최상위 컨텍스트(System Prompt 등)에 접근한다.
딥 셀렉터 (Deep Selector): 복잡한 중첩 구조에서 특정 필드만을 추출하여 컨텍스트에 로드한다. 예를 들어 users{id, role} 구문은 전체 사용자 객체를 로드하는 대신 필요한 정보만을 선택적으로 인출하여 토큰 낭비를 방지한다.15
이러한 상대적 주소 체계는 모델이 전체 문맥을 다시 읽지 않고도 필요한 정보의 위치를 정확히 파악할 수 있게 하여, 어텐션 메커니즘(Attention Mechanism)의 부하를 줄이고 '집중력'을 유지하는 데 기여한다.
3.3 컨텍스트 폴딩 (Context Folding)과 가상 무한 윈도우
재귀적 주소 체계는 컨텍스트 폴딩(Context Folding) 기술을 가능하게 한다.16 에이전트가 긴 추론 과정을 거쳐 중간 결론에 도달했을 때, Denavy 런타임은 이 전체 과정을 하나의 압축된 요약이나 '포인터'로 변환(Folding)한다. 이후의 작업에서는 원본 추론 텍스트 대신 이 포인터만을 컨텍스트에 유지함으로써, 제한된 컨텍스트 윈도우 내에서 사실상 무한에 가까운 작업을 수행할 수 있게 된다.
이는 컴퓨터 메모리 관리의 '페이징(Paging)' 기법과 유사하다. 에이전트는 거대한 지식 베이스나 긴 대화 로그 전체를 메모리에 올리는 대신, Denavy 주소를 통해 필요한 부분(Page)만을 동적으로 스왑(Swap)하며 작업을 진행한다.16
4. 컴파일러 아키텍처: Human DSL to AI IR
Denavy의 컴파일러는 정적인 코드를 기계어로 번역하는 전통적인 컴파일러와 달리, 인간의 의도를 확률적 모델이 이해하고 실행할 수 있는 최적의 프롬프트 스트림으로 변환하는 '컨텍스트 오케스트레이터(Context Orchestrator)' 역할을 수행한다.1
4.1 컴파일 파이프라인 (Compilation Pipeline)
Denavy 소스 코드가 실행 가능한 에이전트 상태로 변환되는 과정은 다음과 같은 다단계 파이프라인을 거친다.
어휘 분석 및 파싱 (Lexical Analysis & Parsing): Denavy 명세를 파싱하여 구문 오류를 검사하고, 불변성 보장을 위한 머클 트리(Merkle Tree) 해시를 검증한다. 상대 경로(^.)는 이 단계에서 내부적으로 절대 경로로 해석되어 링킹(Linking) 준비를 마친다.18
의미 분석 및 최적화 (Semantic Analysis & Optimization):
데드 코드 제거 (Dead Code Elimination): 현재 사용자의 질의나 활성 태스크와 관련 없는 명세 부분을 식별하여 프롬프트 구성에서 제외한다. 이는 토큰 비용을 절감할 뿐만 아니라, 모델이 불필요한 정보에 현혹되는 것(Hallucination)을 방지한다.19
구조적 압축 (Structural Compression): 앞서 언급한 TOON 변환, 기호 매핑 등을 통해 데이터 구조를 고밀도 IR로 변환한다.
중간 표현 생성 (IR Generation): 최적화된 명세를 바탕으로 특정 LLM(예: GPT-4, Claude 3.5)의 특성에 맞는 'Agentic IR'을 생성한다. 이 IR은 시스템 프롬프트, 도구 정의, 메모리 상태, 검증 규칙 등이 구조화된 형태다.20
런타임 실행 (Runtime Execution): 생성된 IR을 LLM에 주입하고, 모델의 출력을 가로채어(Intercept) 도구를 실행하거나 검증 로직을 수행한다.
4.2 생성-검증(Generator-Validator) 아키텍처
Denavy 아키텍처의 핵심은 **생성(Generation)**과 **검증(Validation)**의 철저한 분리다. LLM은 창의적이고 유연한 사고에 능하지만(Generator), 논리적 엄밀성과 규칙 준수에는 취약하다. 반면, 전통적인 코드는 규칙 준수에 완벽하다(Validator). Denavy는 이 둘을 결합하여 'Generator-Validator Gap'을 해소한다.22
생성자 에이전트 (Generator): 높은 온도(Temperature) 설정으로 창의적인 계획 수립과 추론을 담당한다. 압축된 Denavy IR을 입력받아 자연어 또는 코드 형태의 해결책을 제안한다.
검증자 에이전트 (Validator): 낮은 온도 설정 또는 결정론적 코드(Rule-based logic)로 구성된다. 생성자의 출력이 Denavy 명세에 정의된 제약 조건, 타입 시스템, 보안 정책을 준수하는지 엄격하게 검사한다.23 검증자는 생성자와 격리된 메모리 공간에서 실행되어, 생성자의 '환각'에 오염되지 않도록 설계된다(Context Isolation).25
4.3 재귀적 추론 스케일링 (RINS)
컴파일러는 복잡한 작업을 처리하기 위해 재귀적 추론 스케일링(Recursive Inference Scaling, RINS) 기법을 활용한다. 이는 거대한 작업을 한 번의 LLM 호출로 처리하려 하지 않고, 컴파일러가 작업을 재귀적인 하위 태스크로 분해하는 것이다. 각 하위 태스크는 독립적인 모델 호출(Self-Call)을 통해 해결되며, 그 결과는 다시 상위 컨텍스트로 반환된다. 이 과정은 함수형 프로그래밍의 재귀 호출과 유사하며, 이를 통해 고정된 모델 파라미터 내에서 추론 깊이를 가변적으로 확장할 수 있다.27
5. 스펙 불변성과 보안 아키텍처
에이전트 시스템은 외부 데이터나 도구와 상호작용하면서 의도치 않게 원래의 지침에서 벗어나는 '드리프트(Drift)' 현상을 겪거나, 악의적인 '프롬프트 인젝션(Prompt Injection)' 공격에 노출될 수 있다. Denavy는 이를 방지하기 위해 **스펙 불변성(Spec Immutability)**을 아키텍처 레벨에서 강제한다.
5.1 암호학적 불변성 (Cryptographic Immutability)
Denavy 명세는 컴파일 시점에 머클 트리(Merkle Tree) 구조로 변환된다. 명세의 각 블록(제약 조건, 도구 정의, 정책)은 고유한 해시 값을 가지며, 전체 명세는 루트 해시(Root Hash)로 식별된다.30
콘텐츠 주소 지정 (Content-Addressable Code): 런타임에서 에이전트가 특정 지침을 참조할 때, 가변적인 텍스트가 아닌 불변의 해시 값을 통해 참조한다. 만약 런타임 중에 명세 내용이 변경되거나 오염되면 해시 검증이 실패하여 실행이 즉시 중단된다.
디지털 서명 정책 (Signed Policies): "개인정보에 접근하지 말 것"과 같은 핵심 보안 정책은 관리자의 개인키로 디지털 서명된다. 런타임 환경(Validator)은 도구 실행 직전에 이 서명을 검증한다. 프롬프트 인젝션을 통해 외부에서 주입된 명령어는 유효한 서명을 가질 수 없으므로, 원천적으로 실행이 차단된다.31
5.2 실행 가능한 명세와 테스트 내장 (Executable Specifications)
Denavy는 스펙 주도 개발(Spec-Driven Development, SDD) 방법론을 채택하여, 명세 자체가 테스트 케이스를 포함하도록 설계되었다.33
명세 파일 내부에는 Gherkin 문법(Given-When-Then)으로 작성된 테스트 시나리오가 내장된다.35 컴파일러는 이 시나리오를 추출하여 '뉴로-심볼릭 검증(Neuro-Symbolic Validation)' 루틴을 생성한다. 에이전트가 특정 작업을 수행하려고 할 때, 시스템은 먼저 내장된 테스트 케이스를 가상으로 실행(Simulation)하여 에이전트의 계획이 명세를 만족하는지 확인한다. 이는 소프트웨어 공학의 '단위 테스트(Unit Test)'를 런타임 가드레일로 승화시킨 것이다.37
6. 에이전트 격리 및 검증의 성능/비용 최적화
에이전트의 신뢰성을 보장하기 위해 모든 단계를 고성능 LLM으로 검증하는 것은 비용과 지연 시간(Latency) 측면에서 비현실적이다. Denavy는 계층적 검증(Tiered Verification) 전략을 통해 이 딜레마를 해결한다.
6.1 계층적 검증 매트릭스 (Tiered Verification Matrix)
검증 비용과 리스크에 따라 검증의 강도를 동적으로 조절하는 전략이다. Denavy 컴파일러는 명세에 정의된 작업의 중요도(`` 태그)에 따라 적절한 검증 티어를 자동으로 할당한다.40
표 2: 계층적 검증 전략의 비용-성능 트레이드오프
검증 티어 (Tier)
검증 메커니즘
예상 지연시간
비용 (Cost)
적용 사례 (Use Case)
Tier 0 (Syntactic)
정규표현식, 스키마 검증
< 10ms
무시 가능
JSON 형식 검사, 필수 필드 확인
Tier 1 (Light)
BERT/Small LM 분류기
~100ms
낮음
단순 의도 분류, 감성 분석, 금칙어 필터링
Tier 2 (Semantic)
고성능 LLM (Generator와 다른 모델)
1 ~ 3s
높음
복잡한 논리 검증, 코드 리뷰, 보안 정책 대조
Tier 3 (Human)
인간 승인 (HITL)
수 분 ~ 수 시간
매우 높음
금융 거래 실행, 시스템 설정 변경, PII 접근

데이터 기반 재구성: 40
예를 들어, 단순한 데이터 조회 작업은 Tier 0 또는 Tier 1 검증을 거쳐 즉시 실행되지만, 데이터베이스 삭제와 같은 작업은 Tier 2의 심층 검증 후 Tier 3의 인간 승인을 요구하도록 라우팅된다. 연구에 따르면 이러한 계층적 접근은 전체 시스템의 오류율을 최대 **82%**까지 감소시키면서도, 평균 지연 시간 증가를 최소화할 수 있다.43
6.2 적대적 평가 (Adversarial Evaluation)와 자동화된 레드팀
Denavy 아키텍처는 개발 및 배포 단계에서 **적대적 평가(Adversarial Evaluation)**를 내재화한다. 이는 별도의 '레드팀 에이전트(Red Teaming Agent)'가 생성자 에이전트를 지속적으로 공격하는 구조다.25
레드팀 에이전트는 Denavy 명세의 제약 조건을 우회하려는 시도(예: 교묘한 프롬프트 주입, 논리적 함정)를 자동으로 생성하여 주입한다. 이 과정에서 발견된 취약점은 다시 명세의 제약 조건 강화나 검증 로직 개선에 활용된다. 이는 단순한 기능 테스트를 넘어, 에이전트가 예상치 못한 상황에서도 안전하게 동작함을 수학적으로 확률화하여 보증하는 과정이다.
6.3 격리(Isolation)를 통한 보안 강화
검증의 신뢰성을 위해 검증자(Validator)는 생성자(Generator)와 철저히 격리된다. 생성자가 검증자의 판단 기준을 알게 되면 이를 우회하는 방법을 학습할 수 있기 때문이다(Collusion risk). Denavy 런타임은 생성자의 출력을 **살균(Sanitization)**하여 검증자에게 전달하며, 두 에이전트는 서로 다른 프로세스, 심지어 서로 다른 LLM 모델(Model Diversity)을 사용하도록 구성되어 공통된 실패 모드(Common Failure Mode)를 방지한다.26
7. 심층 분석: 고밀도 명세와 컴파일러의 미래
7.1 인지적 부하의 최적화
Denavy의 고밀도 설계는 단순히 토큰 비용을 아끼는 것을 넘어, LLM의 '인지적 부하(Cognitive Load)'를 최적화하는 것이다. 불필요한 구문 요소를 제거하고 정보를 구조화함으로써, 모델의 어텐션 헤드가 정보의 핵심에 집중하도록 유도한다. 이는 인간이 복잡한 문제를 해결할 때 불필요한 정보를 배제하고 핵심 개념만을 기호화하여 사고하는 것과 유사하다.
7.2 컴파일러 기술의 진화
미래의 AI 컴파일러는 코드 변환기를 넘어 **'의미론적 협상자(Semantic Negotiator)'**로 진화할 것이다. 컴파일러는 인간의 의도(Denavy 명세)와 AI 모델의 능력(확률적 분포) 사이에서 최적의 실행 경로를 찾아내는 역할을 수행한다. 또한, 실행 과정에서 발생하는 불확실성을 관리하고, 결과의 신뢰도를 정량적으로 보증하는 시스템 엔지니어링의 핵심 도구가 될 것이다.1
8. 결론
Denavy 리서치는 AI 에이전트 개발이 '프롬프트 엔지니어링'이라는 예술의 영역에서 '시스템 엔지니어링'이라는 공학의 영역으로 넘어가야 함을 시사한다. 고밀도 명세 언어, 재귀적 주소 체계, 불변성 보장, 그리고 계층적 검증 아키텍처는 신뢰할 수 있는 자율 에이전트 시스템을 구축하기 위한 필수적인 요소들이다.
TOON과 같은 고효율 포맷의 도입은 비용 절감과 성능 향상을 동시에 달성할 수 있음을 증명했다. 여기에 프랙탈 구조의 주소 지정과 암호학적 보안이 결합된 Denavy 아키텍처는, AI가 단순한 챗봇을 넘어 복잡한 비즈니스 로직을 안전하고 효율적으로 수행하는 결정론적 소프트웨어 컴포넌트로 자리 잡게 하는 기반이 될 것이다. 이는 곧 다가올 '에이전트 인터넷(Internet of Agents)' 시대를 위한 운영체제의 핵심 커널이 될 것이다.
참고 문헌 및 데이터 소스
토큰 효율성 및 TOON: 2
재귀적 주소 및 프랙탈 구조: 9
에이전트 검증 및 보안: 22
컴파일러 및 명세 아키텍처: 1
일반 에이전트 설계: 53
참고 자료
A Search-Based Compiler to Power the AI-Native Future of Software Engineering - arXiv, 2월 8, 2026에 액세스, https://arxiv.org/html/2510.24799v1
toon-format/toon: Token-Oriented Object Notation (TOON) – Compact, human-readable, schema-aware JSON for LLM prompts. Spec, benchmarks, TypeScript SDK. - GitHub, 2월 8, 2026에 액세스, https://github.com/toon-format/toon
TOON: The data format slashing LLM costs by 50%, 2월 8, 2026에 액세스, https://oguzhanaslann.medium.com/toon-the-data-format-slashing-llm-costs-by-50-ac8d7b808ff6
[Research] I achieved 97% accuracy with 80% context compression - BETTER than using full context (30%) : r/ClaudeAI - Reddit, 2월 8, 2026에 액세스, https://www.reddit.com/r/ClaudeAI/comments/1qdxmu3/research_i_achieved_97_accuracy_with_80_context/
TOON vs JSON: A Token-Optimized Data Format for Reducing LLM Costs | Tensorlake, 2월 8, 2026에 액세스, https://www.tensorlake.ai/blog/toon-vs-json
TOON (Token-Oriented Object Notation): The Guide to Maximizing LLM Efficiency and Accuracy - Vatsal Shah, 2월 8, 2026에 액세스, https://vatsalshah.in/blog/toon-token-oriented-object-notation-guide
TOON vs. JSON vs. YAML: Token Efficiency Breakdown for LLM - Medium, 2월 8, 2026에 액세스, https://medium.com/@ffkalapurackal/toon-vs-json-vs-yaml-token-efficiency-breakdown-for-llm-5d3e5dc9fb9c
Token optimization: The backbone of effective prompt engineering - IBM Developer, 2월 8, 2026에 액세스, https://developer.ibm.com/articles/awb-token-optimization-backbone-of-effective-prompt-engineering/
A Tale of Two Structures: Do LLMs Capture the Fractal Complexity of Language?, 2월 8, 2026에 액세스, https://icml.cc/virtual/2025/poster/44028
NeurIPS Poster Fractal Patterns May Illuminate the Success of Next-Token Prediction, 2월 8, 2026에 액세스, https://neurips.cc/virtual/2024/poster/94393
Fractal Patterns May Illuminate the Success of Next-Token Prediction - OpenReview, 2월 8, 2026에 액세스, https://openreview.net/pdf?id=clAFYReaYE
ASSEMBH User Guide - BS2000 Documentation, 2월 8, 2026에 액세스, https://bs2manuals.ts.fujitsu.com/download/manual/958.1
Learn about relative path syntax - AVEVA™ Documentation, 2월 8, 2026에 액세스, https://docs.aveva.com/bundle/pi-server-f-af-pse/page/1021482.html
Absolute, relative, UNC, and URL paths - ArcMap Resources for ArcGIS Desktop, 2월 8, 2026에 액세스, https://desktop.arcgis.com/en/arcmap/latest/tools/supplement/pathnames-explained-absolute-relative-unc-and-url.htm
Singing a new TOON, a more efficient data format for AI - Epicor User Help Forum, 2월 8, 2026에 액세스, https://www.epiusers.help/t/singing-a-new-toon-a-more-efficient-data-format-for-ai/130773
Recursive Language Models: the paradigm of 2026 - Prime Intellect, 2월 8, 2026에 액세스, https://www.primeintellect.ai/blog/rlm
Understanding AI Agents: Compilers of Human Intent - DEV Community, 2월 8, 2026에 액세스, https://dev.to/sandeep_sharma_2c6860616f/understanding-ai-agents-compilers-of-human-intent-5834
Build an AI Coding Language: My Journey Creating a DSL Parser (Strawberry) - YouTube, 2월 8, 2026에 액세스, https://www.youtube.com/watch?v=pId_14J5TSg
A Token Efficient Language for LLMs - Matt Rickard, 2월 8, 2026에 액세스, https://mattrickard.com/a-token-efficient-language-for-llms
KernelEvolve: Scaling Agentic Kernel Coding for Heterogeneous AI Accelerators at Meta - arXiv, 2월 8, 2026에 액세스, https://arxiv.org/html/2512.23236v1
I built an LLM-assisted compiler that turns architecture specs into production apps (and I'd love your feedback) - Reddit, 2월 8, 2026에 액세스, https://www.reddit.com/r/Compilers/comments/1piiv4x/i_built_an_llmassisted_compiler_that_turns/
Generator-Validator Gap in AI Evaluation - Emergent Mind, 2월 8, 2026에 액세스, https://www.emergentmind.com/topics/generator-validator-gap
Validating multi-agent AI systems: From modular testing to system-level governance - PwC, 2월 8, 2026에 액세스, https://www.pwc.com/us/en/services/audit-assurance/library/validating-multi-agent-ai-systems.html
The AI Agent Behavioral Validation Testing Playbook - Galileo AI: The AI Observability and Evaluation Platform, 2월 8, 2026에 액세스, https://galileo.ai/learn/ai-observability/ai-agent-testing-behavioral-validation
Why AI Agent Architecture Matters More Than You Think: A Security Deep Dive | Rasa Blog, 2월 8, 2026에 액세스, https://rasa.com/blog/ai-agent-architecture-security-deep-dive
How to Secure Agentic AI With Hardened Runtime Isolation - Edera, 2월 8, 2026에 액세스, https://edera.dev/stories/securing-agentic-ai-systems-with-hardened-runtime-isolation
Recursive Language Models w/ Alex Zhang - YouTube, 2월 8, 2026에 액세스, https://www.youtube.com/watch?v=6Dr3SUmHFco
Recursive Inference Scaling: A Winning Path to Scalable Inference in Language and Multimodal Systems - arXiv, 2월 8, 2026에 액세스, https://arxiv.org/html/2502.07503v2
NeurIPS Poster Recursive Inference Scaling: A Winning Path to Scalable Inference in Language and Multimodal Systems, 2월 8, 2026에 액세스, https://neurips.cc/virtual/2025/poster/117101
Provenance Verification of AI-Generated Images via a Perceptual Hash Registry Anchored on Blockchain - arXiv, 2월 8, 2026에 액세스, https://arxiv.org/html/2602.02412v1
Attestation in the C2PA Framework, 2월 8, 2026에 액세스, https://spec.c2pa.org/specifications/specifications/1.4/attestations/attestation.html
Immutable watermarking for authenticating and verifying AI-generated output, 2월 8, 2026에 액세스, https://patents.justia.com/patent/11514365
Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl - Martin Fowler, 2월 8, 2026에 액세스, https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants - arXiv, 2월 8, 2026에 액세스, https://arxiv.org/html/2602.00180v1
Writing scenarios with Gherkin syntax | CucumberStudio Documentation, 2월 8, 2026에 액세스, https://support.smartbear.com/cucumberstudio/docs/bdd/write-gherkin-scenarios.html
Json To Gherkin Conversion Agent | Google Cloud AI agent finder, 2월 8, 2026에 액세스, https://cloud.withgoogle.com/agentfinder/product/9cf1d513-737a-4992-98ba-e0a49536287a/
Beyond Vibe Coding: Using TLA+ and Executable Specifications with Claude, 2월 8, 2026에 액세스, https://shahbhat.medium.com/beyond-vibe-coding-using-tla-and-executable-specifications-with-claude-51df2a9460ff
Kinde Executable Specs: Turning Plain English into Running Systems, 2월 8, 2026에 액세스, https://kinde.com/learn/ai-for-software-engineering/best-practice/executable-specs-turning-plain-english-into-running-systems/
Large Language Models for Unit Test Generation: Achievements, Challenges, and the Road Ahead - arXiv, 2월 8, 2026에 액세스, https://arxiv.org/html/2511.21382v1
Large-Scale AI Safety Through Truth Ensembles and Consensus Verification - GitHub Gist, 2월 8, 2026에 액세스, https://gist.github.com/bigsnarfdude/21cbae2ef56c01e0f53c223b0e2ca0b1
Optimized Financial Planning: Integrating Individual and Cooperative Budgeting Models with LLM Recommendations, 2월 8, 2026에 액세스, https://zaguan.unizar.es/record/145276/files/texto_completo.pdf
FusionGraphRAG: An Adaptive Retrieval-Augmented Generation Framework for Complex Disease Management in the Elderly - MDPI, 2월 8, 2026에 액세스, https://www.mdpi.com/2078-2489/17/2/138
Mitigating LLM Hallucinations: A Comprehensive ... - Preprints.org, 2월 8, 2026에 액세스, https://www.preprints.org/manuscript/202505.1955/download/final_file
When Hallucination Costs Millions: Benchmarking AI Agents in High-Stakes Adversarial Financial Markets - arXiv, 2월 8, 2026에 액세스, https://arxiv.org/html/2510.00332v2
AgenTRIM: Tool Risk Mitigation for Agentic AI - arXiv, 2월 8, 2026에 액세스, https://arxiv.org/html/2601.12449v1
TOON: Token Oriented Object Notation for Efficient LLM Prompts | by Nabaraj Ghimire, 2월 8, 2026에 액세스, https://medium.com/@nabarajghimire222/toon-token-oriented-object-notation-a-llm-friendly-token-structure-89e134eeba5d
The Rise of TOON: Token-Oriented Object Notation for Efficient Large Language Model (LLM) Workflows | by Cengizhan Bayram | Medium, 2월 8, 2026에 액세스, https://medium.com/@cenghanbayram35/the-rise-of-toon-token-oriented-object-notation-for-efficient-large-language-model-llm-workflows-95c4fd9f5689
Recursive neural programs: A differentiable framework for learning compositional part-whole hierarchies and image grammars - PMC, 2월 8, 2026에 액세스, https://pmc.ncbi.nlm.nih.gov/articles/PMC10637337/
AI and Language: Learning from Fractal Structures - AIGeneration.blog, 2월 8, 2026에 액세스, https://aigeneration.blog/2025/03/30/ai-and-language-learning-from-fractal-structures/
[2512.18940] FASTRIC: Prompt Specification Language for Verifiable LLM Interactions, 2월 8, 2026에 액세스, https://arxiv.org/abs/2512.18940
A Layered Protocol Architecture for the Internet of Agents - arXiv, 2월 8, 2026에 액세스, https://arxiv.org/html/2511.19699v3
Building Reliable AI Agents Requires Compiler Like Systems - Aria Attar, 2월 8, 2026에 액세스, https://ariaattar.com/LLMCompiler
Demystifying evals for AI agents - Anthropic, 2월 8, 2026에 액세스, https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
Understanding AI Agent Security - Promptfoo, 2월 8, 2026에 액세스, https://www.promptfoo.dev/blog/agent-security/
Multi-Agent System Patterns: Architectures, Roles & Design Guide - Medium, 2월 8, 2026에 액세스, https://medium.com/@mjgmario/multi-agent-system-patterns-a-unified-guide-to-designing-agentic-architectures-04bb31ab9c41
Agent architecture: How AI decision-making drives business impact - Retool Blog, 2월 8, 2026에 액세스, https://retool.com/blog/agent-architecture
