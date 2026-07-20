import { Request, Response, NextFunction } from 'express';

const idempotencyCache = new Map<string, any>();

export function idempotencyGuard(req: Request, res: any, next: NextFunction) {
  const idempotencyKey = req.headers['idempotency-key'] as string;

  if (!idempotencyKey) {
    return next();
  }

  // 3. Idempotency Check
  if (idempotencyCache.has(idempotencyKey)) {
    console.log(`Duplicate request detected for key: ${idempotencyKey}.`);
    return res.status(200).json(idempotencyCache.get(idempotencyKey));
  }

  res.saveToIdempotencyCache = (data: any) => {
    idempotencyCache.set(idempotencyKey, data);
  };

  next();
}