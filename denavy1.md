1. 거시적 관점: 연합형 레지스트리 (Ecosystem)
각 레지스트리(예: 서울, 부산)는 거대한 생태계 안에서 독립적으로 존재하며, 타 프로젝트 및 타 레지스트리의 코드를 직접 수정할 수 없는 읽기 전용(Read-Only) 상태를 기본으로 합니다.
상호작용 방식은 딱 세 가지입니다.
Import: 남의 기능을 수정 없이 그대로 가져다 씁니다.
Request: 원본에 버그나 개선 사항을 제안합니다. (.req 파일 전송)
Fork: 원본을 내 프로젝트로 복제하여 독자적으로 진화시킵니다.
2. 미시적 관점: 3계층 평행 미러링 (Internal Structure)
프로젝트 내부는 철저하게 역할이 분리된 3개의 폴더로 나뉘며, 하위 도메인 구조는 똑같이 일치해야 합니다.
/dna (규칙 Layer): 변하지 않는 데이터 타입과 제약 조건. 상속을 통해 관리됩니다.
registry-root.dna: 생태계 공통 통신 규약 및 기호 정의
project-root.dna: 해당 프로젝트만의 기술 스택 (Go, DB 등)
domain/user.dna: 유저 도메인의 데이터 스키마
/spec (설계도 Layer): 비즈니스 로직의 흐름. 범규님이 직접 읽고 승인하는 문서입니다.
/src (구현체 Layer): AI가 spec을 보고 만들어낸 실제 코드. 사람은 절대 직접 수정하지 않습니다.
3. 에이전트 작업 흐름과 TOON 문법 (Workflow)
에이전트는 상주하지 않고 필요할 때마다 프롬프트와 함께 생성됩니다. 이때 프롬프트에는 root.dna에 정의된 아래의 8대 기호 해독표(Bootloader)가 주입됩니다.
@bootloader
    def symbol:
        !  : "Invariant (필수 제약/검증)"       # 예: ! password.length > 8
        ?  : "Decision (조건 분기/IF)"         # 예: ? email_exists
        >  : "Execute (함수 실행/API 호출)"      # 예: > DB.save(user)
        <- : "Assign (변수 할당)"              # 예: hash <- Crypto.hash(pw)
        * : "Loop (반복/순회)"                # 예: * item in cart
        => : "Return (결과 반환/에러 전파)"      # 예: => Error("FAIL")
        @  : "Import (외부 참조)"              # 예: @ User_DNA
        <: : "Inherit (상속)"                 # 예: Admin <: User
에이전트는 이 기호로 작성된 spec 파일과 dna 파일을 읽고, src 폴더에 코드를 생성한 뒤 소멸합니다.

