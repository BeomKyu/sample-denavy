# FILE: sample-denavy/spec/wallet/charge.spec

import dna/wallet/wallet.dna (Wallet, Transaction, TxType)

struct ChargeReq
    wallet_id: uuid
    amount: u64 @min(100) # Minimum charge amount 100

fn charge(req: ChargeReq) -> Result<Wallet, Error>
    # 1. Validation & Load
    target <- Wallet.findById(req.wallet_id) !=>! Err(WalletNotFound)

    # 2. State Mutation
    target.balance <- target.balance + req.amount

    # 3. Log History
    > Transaction.save(Transaction(
        wallet_id: target.id,
        type: TxType.Charge,
        amount: req.amount,
        memo: "Point Charge"
    ))

    # 4. Save & Return
    > Wallet.save(target)
    => Ok(target)
